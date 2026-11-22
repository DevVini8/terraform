"""
FASE 3: Módulo de Carga no Banco Relacional PostgreSQL Aiven & SQLite Portátil (load.py)
Executa a criação do esquema Estrela (schema.sql) e realiza a carga em batches (chunking):
  1. Em banco relacional SQLite autocontido (`data/processed/dw_violencia_interseccional.db`) e Dump SQL (`dump_dw_violencia_interseccional.sql`) para acesso imediato sem necessidade de credenciais externas.
  2. Em serviço gerenciado PostgreSQL 16 na Aiven Cloud (via `DATABASE_URL` no `.env`), verificando continuamente o consumo de armazenamento para respeitar o limite de 1 GB da Aiven.
"""
import logging
import sqlite3
from pathlib import Path
from typing import Dict
import pandas as pd
from sqlalchemy import create_engine, text

from etl.config import (
    CHUNK_SIZE,
    MAX_DB_SIZE_MB,
    SCHEMA_SQL_PATH,
    PROCESSED_DIR,
    SQLITE_DB_PATH,
    SQL_DUMP_PATH,
    get_database_url,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | [LOAD] %(message)s",
)
logger = logging.getLogger(__name__)

LOAD_ORDER = [
    "dim_tempo",
    "dim_localidade",
    "dim_perfil_vitima",
    "dim_contexto_crime",
    "fato_violencia_sinesp",
    "fato_vitimas_fogo_cruzado",
]


def estimate_payload_size_mb(tables: Dict[str, pd.DataFrame]) -> float:
    """Calcula a memória total estimada (em MB) das tabelas do Star Schema antes da carga."""
    total_bytes = sum(df.memory_usage(deep=True).sum() for df in tables.values())
    return round(total_bytes / (1024 * 1024), 2)


def export_star_schema_locally(tables: Dict[str, pd.DataFrame], out_dir: Path = PROCESSED_DIR) -> None:
    """
    Salva as tabelas do Esquema Estrela na pasta /data/processed em CSV para auditoria,
    reprodutibilidade rápida e cache do Dashboard no Streamlit Cloud.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    for table_name, df in tables.items():
        csv_path = out_dir / f"{table_name}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8")
        logger.info(f"Tabela exportada localmente: {csv_path} ({len(df):,} linhas)")


def build_sqlite_warehouse_and_dump(
    tables: Dict[str, pd.DataFrame],
    sqlite_path: Path = SQLITE_DB_PATH,
    sql_dump_path: Path = SQL_DUMP_PATH,
) -> Path:
    """
    Constrói o banco de dados relacional SQLite3 completo com todas as chaves primárias (PK),
    chaves estrangeiras (FK), índices B-Tree e as 2 Views Analíticas do Esquema Estrela,
    além de exportar o arquivo de dump SQL completo (.sql) pronto para importação direta.
    """
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    if sqlite_path.exists():
        sqlite_path.unlink()

    sqlite_ddl = """
    PRAGMA foreign_keys = ON;

    CREATE TABLE dim_tempo (
        id_tempo        INTEGER PRIMARY KEY,
        data_completa   DATE NOT NULL UNIQUE,
        ano             SMALLINT NOT NULL,
        mes             SMALLINT NOT NULL,
        nome_mes        VARCHAR(20) NOT NULL,
        trimestre       SMALLINT NOT NULL,
        semestre        SMALLINT NOT NULL
    );
    CREATE INDEX idx_dim_tempo_ano_mes ON dim_tempo (ano, mes);

    CREATE TABLE dim_localidade (
        id_localidade   INTEGER PRIMARY KEY,
        regiao          VARCHAR(20) NOT NULL,
        uf              CHAR(2) NOT NULL,
        estado          VARCHAR(50) NOT NULL,
        municipio       VARCHAR(120) NOT NULL,
        bairro          VARCHAR(120) DEFAULT 'NÃO ESPECIFICADO',
        UNIQUE (uf, municipio, bairro)
    );
    CREATE INDEX idx_dim_localidade_regiao_uf ON dim_localidade (regiao, uf);
    CREATE INDEX idx_dim_localidade_municipio ON dim_localidade (municipio);

    CREATE TABLE dim_perfil_vitima (
        id_perfil               INTEGER PRIMARY KEY,
        genero                  VARCHAR(45) NOT NULL,
        macro_genero            VARCHAR(25) NOT NULL,
        raca_cor                VARCHAR(35) NOT NULL,
        faixa_etaria            VARCHAR(45) NOT NULL,
        tipo_pessoa             VARCHAR(35) NOT NULL,
        grupo_interseccional    VARCHAR(80) NOT NULL,
        UNIQUE (genero, raca_cor, faixa_etaria, tipo_pessoa)
    );
    CREATE INDEX idx_dim_perfil_interseccional ON dim_perfil_vitima (macro_genero, raca_cor, grupo_interseccional);

    CREATE TABLE dim_contexto_crime (
        id_contexto         INTEGER PRIMARY KEY,
        fonte_dados         VARCHAR(30) NOT NULL,
        tipo_evento         VARCHAR(150) NOT NULL,
        arma                VARCHAR(80) NOT NULL,
        agente_seguranca    VARCHAR(80) NOT NULL,
        acao_policial       BOOLEAN NOT NULL DEFAULT 0,
        presenca_agente     BOOLEAN NOT NULL DEFAULT 0,
        chacina             BOOLEAN NOT NULL DEFAULT 0,
        circunstancia       VARCHAR(100) NOT NULL DEFAULT 'Não especificada',
        local_ocorrencia    VARCHAR(100) NOT NULL DEFAULT 'Não especificado',
        UNIQUE (fonte_dados, tipo_evento, arma, agente_seguranca, acao_policial, presenca_agente, chacina, circunstancia, local_ocorrencia)
    );
    CREATE INDEX idx_dim_contexto_evento ON dim_contexto_crime (fonte_dados, tipo_evento);

    CREATE TABLE fato_violencia_sinesp (
        id_fato_sinesp      INTEGER PRIMARY KEY,
        id_tempo            INTEGER NOT NULL REFERENCES dim_tempo(id_tempo),
        id_localidade       INTEGER NOT NULL REFERENCES dim_localidade(id_localidade),
        id_contexto         INTEGER NOT NULL REFERENCES dim_contexto_crime(id_contexto),
        vitimas_feminino    INTEGER NOT NULL DEFAULT 0,
        vitimas_masculino   INTEGER NOT NULL DEFAULT 0,
        vitimas_nao_inf     INTEGER NOT NULL DEFAULT 0,
        total_vitimas       INTEGER NOT NULL DEFAULT 0,
        total_ocorrencias   NUMERIC(12, 2) NOT NULL DEFAULT 0,
        total_peso          NUMERIC(12, 3) NOT NULL DEFAULT 0
    );
    CREATE INDEX idx_fato_sinesp_tempo_loc ON fato_violencia_sinesp (id_tempo, id_localidade);
    CREATE INDEX idx_fato_sinesp_contexto ON fato_violencia_sinesp (id_contexto);

    CREATE TABLE fato_vitimas_fogo_cruzado (
        id_fato_fc          INTEGER PRIMARY KEY,
        vitima_hash_lgpd    CHAR(16) NOT NULL,
        ocorrencia_hash     CHAR(16) NOT NULL,
        id_tempo            INTEGER NOT NULL REFERENCES dim_tempo(id_tempo),
        id_localidade       INTEGER NOT NULL REFERENCES dim_localidade(id_localidade),
        id_perfil           INTEGER NOT NULL REFERENCES dim_perfil_vitima(id_perfil),
        id_contexto         INTEGER NOT NULL REFERENCES dim_contexto_crime(id_contexto),
        situacao_vitima     VARCHAR(20) NOT NULL,
        is_fatal            SMALLINT NOT NULL,
        idade_vitima        SMALLINT,
        lat_aprox           NUMERIC(6, 2),
        lon_aprox           NUMERIC(6, 2)
    );
    CREATE INDEX idx_fato_fc_tempo_loc ON fato_vitimas_fogo_cruzado (id_tempo, id_localidade);
    CREATE INDEX idx_fato_fc_perfil ON fato_vitimas_fogo_cruzado (id_perfil);
    CREATE INDEX idx_fato_fc_contexto ON fato_vitimas_fogo_cruzado (id_contexto);

    CREATE VIEW vw_resumo_interseccional_fogo_cruzado AS
    SELECT
        t.ano,
        t.mes,
        t.nome_mes,
        t.trimestre,
        l.regiao,
        l.uf,
        l.estado,
        l.municipio,
        l.bairro,
        p.genero,
        p.macro_genero,
        p.raca_cor,
        p.faixa_etaria,
        p.tipo_pessoa,
        p.grupo_interseccional,
        c.tipo_evento AS motivo_principal,
        c.acao_policial,
        c.presenca_agente,
        c.chacina,
        c.circunstancia,
        c.local_ocorrencia,
        f.situacao_vitima,
        f.is_fatal,
        f.idade_vitima,
        f.lat_aprox,
        f.lon_aprox
    FROM fato_vitimas_fogo_cruzado f
    JOIN dim_tempo t          ON f.id_tempo = t.id_tempo
    JOIN dim_localidade l     ON f.id_localidade = l.id_localidade
    JOIN dim_perfil_vitima p  ON f.id_perfil = p.id_perfil
    JOIN dim_contexto_crime c ON f.id_contexto = c.id_contexto;

    CREATE VIEW vw_resumo_violencia_sinesp AS
    SELECT
        t.ano,
        t.mes,
        t.nome_mes,
        t.trimestre,
        l.regiao,
        l.uf,
        l.estado,
        l.municipio,
        c.tipo_evento,
        c.arma,
        c.agente_seguranca,
        f.vitimas_feminino,
        f.vitimas_masculino,
        f.vitimas_nao_inf,
        f.total_vitimas,
        f.total_ocorrencias,
        f.total_peso
    FROM fato_violencia_sinesp f
    JOIN dim_tempo t          ON f.id_tempo = t.id_tempo
    JOIN dim_localidade l     ON f.id_localidade = l.id_localidade
    JOIN dim_contexto_crime c ON f.id_contexto = c.id_contexto;
    """

    with sqlite3.connect(sqlite_path) as conn:
        conn.executescript(sqlite_ddl)
        for table_name in LOAD_ORDER:
            if table_name in tables:
                df = tables[table_name]
                df.to_sql(table_name, conn, if_exists="append", index=False)
        conn.commit()

        # Exporta o Dump SQL completo (DDL + INSERTs)
        with open(sql_dump_path, "w", encoding="utf-8") as f_dump:
            f_dump.write("-- =============================================================================\n")
            f_dump.write("-- ENTREGÁVEL 3: DUMP SQL COMPLETO DO BANCO DE DADOS (STAR SCHEMA + DADOS)\n")
            f_dump.write("-- Banco: dw_violencia_interseccional (ODS 5 & ODS 18 - Capitais 2025)\n")
            f_dump.write("-- =============================================================================\n\n")
            for line in conn.iterdump():
                f_dump.write(f"{line}\n")

    size_kb = round(sqlite_path.stat().st_size / 1024, 2)
    logger.info(
        f"Banco relacional SQLite3 construído com sucesso em: {sqlite_path} ({size_kb} KB) "
        f"e Dump SQL salvo em: {sql_dump_path}"
    )
    return sqlite_path


def load_to_aiven_postgres(
    tables: Dict[str, pd.DataFrame],
    database_url: str = "",
    chunk_size: int = CHUNK_SIZE,
) -> bool:
    """
    Conecta ao PostgreSQL na Aiven via SQLAlchemy, aplica o DDL (schema.sql) e
    carrega as dimensões e tabelas fato utilizando chunking (`chunksize=5000` e `method='multi'`).
    """
    db_url = database_url or get_database_url()
    est_mb = estimate_payload_size_mb(tables)
    logger.info(
        f"Volume estimado do Star Schema: {est_mb} MB "
        f"(Limite seguro configurado: {MAX_DB_SIZE_MB} MB / 1024 MB Aiven Free Tier)."
    )

    if est_mb > MAX_DB_SIZE_MB:
        raise ValueError(
            f"Volume estimado ({est_mb} MB) excede o limite de segurança ({MAX_DB_SIZE_MB} MB) para o banco Aiven 1 GB!"
        )

    if not db_url:
        logger.warning(
            "Variável DATABASE_URL / DB_HOST não configurada com instância ativa da Aiven no .env. "
            "O banco relacional local SQLite (dw_violencia_interseccional.db) e o Dump SQL foram gerados em /data/processed."
        )
        return False

    logger.info("Conectando ao banco PostgreSQL na Aiven (SSL habilitado)...")
    engine = create_engine(db_url, pool_pre_ping=True)

    with engine.begin() as conn:
        if SCHEMA_SQL_PATH.exists():
            logger.info(f"Executando script DDL do Star Schema: {SCHEMA_SQL_PATH}")
            sql_script = SCHEMA_SQL_PATH.read_text(encoding="utf-8")
            conn.execute(text(sql_script))

    for table_name in LOAD_ORDER:
        if table_name not in tables:
            continue
        df = tables[table_name]
        logger.info(f"Carregando '{table_name}' ({len(df):,} linhas) em chunks de {chunk_size}...")
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=chunk_size,
            method="multi",
        )
        logger.info(f"Carga de '{table_name}' concluída com sucesso.")

    with engine.connect() as conn:
        db_size = conn.execute(
            text("SELECT pg_size_pretty(pg_database_size(current_database()));")
        ).scalar()
        logger.info(f"Tamanho total ocupado no PostgreSQL Aiven após a carga: {db_size} (Limite: 1 GB).")

    return True

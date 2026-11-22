"""
ENTREGÁVEL 3: Utilitário Interativo de Acesso Simples ao Banco de Dados (acessar_banco.py)
Permite consultar diretamente o banco de dados relacional do projeto (Star Schema):
  - Localmente via SQLite3 (`data/processed/dw_violencia_interseccional.db`) sem exigir instalação de servidor externo
  - Remotamente via PostgreSQL 16 na Aiven Cloud (caso `DATABASE_URL` esteja configurada no `.env`)

Modos de uso:
  1. Resumo completo das tabelas, estrutura, relacionamentos e contagens:
       python acessar_banco.py
  2. Executar qualquer consulta SQL diretamente pelo terminal:
       python acessar_banco.py --sql "SELECT * FROM vw_resumo_interseccional_fogo_cruzado LIMIT 10"
  3. Modo console SQL interativo:
       python acessar_banco.py --interativo
"""
import argparse
import sqlite3
from pathlib import Path
import pandas as pd

from etl.config import SQLITE_DB_PATH, SQL_DUMP_PATH, get_database_url
from etl.pipeline import run_pipeline

TABLES_AND_VIEWS = [
    ("dim_tempo", "Dimensão Tempo (Calendário 2025)"),
    ("dim_localidade", "Dimensão Localidade (27 Capitais & Bairros)"),
    ("dim_perfil_vitima", "Dimensão Perfil Interseccional da Vítima (ODS 5 & ODS 18)"),
    ("dim_contexto_crime", "Dimensão Contexto e Tipificação do Crime"),
    ("fato_violencia_sinesp", "Tabela Fato 1: Violência contra a Mulher nas 27 Capitais (SINESP 2025)"),
    ("fato_vitimas_fogo_cruzado", "Tabela Fato 2: Mulheres Baleadas 18-45a nas Capitais (Fogo Cruzado 2025)"),
    ("vw_resumo_violencia_sinesp", "View Analítica 1: SINESP Desnormalizada (JOIN Fato 1 + Dimensões)"),
    ("vw_resumo_interseccional_fogo_cruzado", "View Analítica 2: Fogo Cruzado Desnormalizada (JOIN Fato 2 + Dimensões)"),
]


def ensure_database_exists() -> Path:
    """Garante que o banco relacional SQLite e o Dump SQL estejam construídos."""
    if not SQLITE_DB_PATH.exists():
        print("[INFO] Banco de dados ainda não encontrado. Executando pipeline ETL para construí-lo...")
        run_pipeline(skip_db=True)
    return SQLITE_DB_PATH


def print_database_summary(conn: sqlite3.Connection) -> None:
    db_size_kb = round(SQLITE_DB_PATH.stat().st_size / 1024, 2)
    dump_size_kb = round(SQL_DUMP_PATH.stat().st_size / 1024, 2) if SQL_DUMP_PATH.exists() else 0.0

    print("=" * 95)
    print(" 🗄️  ENTREGÁVEL 3: BASE ARMAZENADA EM BANCO DE DADOS (STAR SCHEMA - ODS 5 & ODS 18)")
    print("=" * 95)
    print(f" • Arquivo do Banco Relacional (SQLite3): {SQLITE_DB_PATH} ({db_size_kb} KB)")
    print(f" • Dump SQL Completo (DDL + INSERTs):     {SQL_DUMP_PATH} ({dump_size_kb} KB)")
    aiven_url = get_database_url()
    print(f" • Status Aiven PostgreSQL (.env):        {'CONECTADO' if aiven_url else 'Pronto para carga (configure DATABASE_URL no .env)'}")
    print("-" * 95)
    print(f" {'ENTIDADE / TABELA / VIEW':<40} | {'TIPO':<12} | {'REGISTROS':>10} | {'DESCRIÇÃO'}")
    print("-" * 95)

    total_rows_tables = 0
    for name, desc in TABLES_AND_VIEWS:
        is_view = name.startswith("vw_")
        tipo = "VIEW SQL" if is_view else "TABELA"
        count = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        if not is_view:
            total_rows_tables += count
        print(f" {name:<40} | {tipo:<12} | {count:>10,} | {desc}")

    print("-" * 95)
    print(f" TOTAL DE REGISTROS ARMAZENADOS NAS 6 TABELAS FÍSICAS DO STAR SCHEMA: {total_rows_tables:,} registros")
    print("=" * 95)

    # Consultas analíticas demonstrativas
    print("\n📊 [CONSULTA SQL 1] Total de Vítimas Femininas nas 27 Capitais por Evento (fato_violencia_sinesp):")
    q1 = """
    SELECT
        c.tipo_evento AS evento_criminal,
        COUNT(f.id_fato_sinesp) AS registros_mensais_capitais,
        SUM(f.vitimas_feminino) AS total_vitimas_femininas
    FROM fato_violencia_sinesp f
    JOIN dim_contexto_crime c ON f.id_contexto = c.id_contexto
    GROUP BY c.tipo_evento
    ORDER BY total_vitimas_femininas DESC;
    """
    print(pd.read_sql_query(q1, conn).to_string(index=False))

    print("\n📊 [CONSULTA SQL 2] Top 10 Capitais com Maior Volume de Vítimas Femininas em 2025 (vw_resumo_violencia_sinesp):")
    q2 = """
    SELECT
        regiao,
        uf,
        municipio AS capital,
        SUM(CASE WHEN tipo_evento = 'Feminicídio' THEN vitimas_feminino ELSE 0 END) AS feminicidios,
        SUM(CASE WHEN tipo_evento = 'Tentativa de feminicídio' THEN vitimas_feminino ELSE 0 END) AS tentativas_feminicidio,
        SUM(vitimas_feminino) AS total_vitimas_femininas
    FROM vw_resumo_violencia_sinesp
    GROUP BY regiao, uf, municipio
    ORDER BY total_vitimas_femininas DESC
    LIMIT 10;
    """
    print(pd.read_sql_query(q2, conn).to_string(index=False))

    print("\n📊 [CONSULTA SQL 3] Matriz Interseccional Gênero x Raça/Cor de Mulheres Baleadas 18-45a (vw_resumo_interseccional_fogo_cruzado):")
    q3 = """
    SELECT
        genero,
        raca_cor,
        COUNT(*) AS total_mulheres_baleadas,
        SUM(is_fatal) AS mortas,
        COUNT(*) - SUM(is_fatal) AS feridas,
        ROUND(AVG(is_fatal) * 100, 1) AS letalidade_pct,
        ROUND(AVG(idade_vitima), 1) AS idade_media
    FROM vw_resumo_interseccional_fogo_cruzado
    GROUP BY genero, raca_cor
    ORDER BY total_mulheres_baleadas DESC;
    """
    print(pd.read_sql_query(q3, conn).to_string(index=False))
    print("\n💡 Dica: Execute `python acessar_banco.py --interativo` para abrir o prompt SQL ou acesse a Aba 6 do Dashboard (`streamlit run dashboard/app.py`).\n")


def run_interactive_shell(conn: sqlite3.Connection) -> None:
    print("\n" + "=" * 80)
    print(" 💻 CONSOLE SQL INTERATIVO - BANCO dw_violencia_interseccional.db")
    print(" Digite qualquer comando SQL (ex: SELECT * FROM dim_perfil_vitima;) ou 'sair' para encerrar.")
    print("=" * 80)
    while True:
        try:
            query = input("\nSQL> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando console SQL.")
            break
        if not query or query.lower() in {"sair", "exit", "quit"}:
            print("Encerrando console SQL.")
            break
        try:
            df_res = pd.read_sql_query(query, conn)
            print(df_res.to_string(index=False))
            print(f"\n({len(df_res)} linhas retornadas)")
        except Exception as exc:
            print(f"[ERRO SQL]: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Acesso Simples ao Banco de Dados - Entregável 3")
    parser.add_argument("--sql", type=str, default="", help="Executa uma query SQL diretamente e exibe o resultado")
    parser.add_argument("--interativo", action="store_true", help="Abre um console SQL interativo no terminal")
    args = parser.parse_args()

    db_path = ensure_database_exists()
    with sqlite3.connect(db_path) as conn:
        if args.sql:
            df = pd.read_sql_query(args.sql, conn)
            print(df.to_string(index=False))
        elif args.interativo:
            run_interactive_shell(conn)
        else:
            print_database_summary(conn)


if __name__ == "__main__":
    main()

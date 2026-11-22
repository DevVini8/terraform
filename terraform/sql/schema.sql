-- =============================================================================
-- FASE 3: Modelagem Dimensional (Star Schema / Esquema Estrela)
-- Banco de Dados Relacional: PostgreSQL (Aiven Free Tier - Limite 1 GB)
-- Tema: Análise Interseccional da Violência no Brasil (ODS 5 & ODS 18)
-- Fontes:
--   1. SINESP / MJSP (fonte original.xlsx)
--   2. Instituto Fogo Cruzado (complemento fogo cruzado.xlsx)
-- =============================================================================

-- Limpeza opcional para recarga idempotente
DROP VIEW IF EXISTS vw_resumo_interseccional_fogo_cruzado CASCADE;
DROP VIEW IF EXISTS vw_resumo_violencia_sinesp CASCADE;
DROP TABLE IF EXISTS fato_vitimas_fogo_cruzado CASCADE;
DROP TABLE IF EXISTS fato_violencia_sinesp CASCADE;
DROP TABLE IF EXISTS dim_contexto_crime CASCADE;
DROP TABLE IF EXISTS dim_perfil_vitima CASCADE;
DROP TABLE IF EXISTS dim_localidade CASCADE;
DROP TABLE IF EXISTS dim_tempo CASCADE;

-- -----------------------------------------------------------------------------
-- 1. DIMENSÃO TEMPO (dim_tempo)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_tempo (
    id_tempo        INTEGER PRIMARY KEY,           -- Formato YYYYMMDD (ex: 20250131)
    data_completa   DATE NOT NULL UNIQUE,
    ano             SMALLINT NOT NULL,
    mes             SMALLINT NOT NULL,
    nome_mes        VARCHAR(20) NOT NULL,
    trimestre       SMALLINT NOT NULL,
    semestre        SMALLINT NOT NULL
);

CREATE INDEX idx_dim_tempo_ano_mes ON dim_tempo (ano, mes);

-- -----------------------------------------------------------------------------
-- 2. DIMENSÃO LOCALIDADE (dim_localidade)
-- Nota LGPD: Endereço exato removido e coordenadas truncadas/omitidas para
-- evitar reidentificação espacial de vítimas em microáreas.
-- -----------------------------------------------------------------------------
CREATE TABLE dim_localidade (
    id_localidade   SERIAL PRIMARY KEY,
    regiao          VARCHAR(20) NOT NULL,          -- Norte, Nordeste, Sudeste, Sul, Centro-Oeste
    uf              CHAR(2) NOT NULL,              -- Sigla da UF (ex: BA, PE, PA, RJ, SP)
    estado          VARCHAR(50) NOT NULL,          -- Nome da UF
    municipio       VARCHAR(120) NOT NULL,         -- Município / Cidade padronizado
    bairro          VARCHAR(120) DEFAULT 'NÃO ESPECIFICADO',
    UNIQUE (uf, municipio, bairro)
);

CREATE INDEX idx_dim_localidade_regiao_uf ON dim_localidade (regiao, uf);
CREATE INDEX idx_dim_localidade_municipio ON dim_localidade (municipio);

-- -----------------------------------------------------------------------------
-- 3. DIMENSÃO PERFIL DA VÍTIMA (dim_perfil_vitima)
-- Alinhada aos indicadores interseccionais da ODS 5 (Gênero) e ODS 18 (Raça/Cor)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_perfil_vitima (
    id_perfil               SERIAL PRIMARY KEY,
    genero                  VARCHAR(45) NOT NULL,  -- Mulher cis, Mulher trans e travesti, Homem cis, Feminino, Masculino, Não informado
    macro_genero            VARCHAR(25) NOT NULL,  -- Feminino, Masculino, Trans/Travesti, Não informado
    raca_cor                VARCHAR(35) NOT NULL,  -- Negra, Branca, Indígena, Amarela, Não identificado
    faixa_etaria            VARCHAR(45) NOT NULL,  -- Criança, Adolescente, Adulto, Idoso, Não informado
    tipo_pessoa             VARCHAR(35) NOT NULL,  -- Civil, Agente de Segurança, Não informado
    grupo_interseccional    VARCHAR(80) NOT NULL,  -- Ex: "Mulher Negra", "Mulher Trans/Travesti", "Homem Negro", etc.
    UNIQUE (genero, raca_cor, faixa_etaria, tipo_pessoa)
);

CREATE INDEX idx_dim_perfil_interseccional ON dim_perfil_vitima (macro_genero, raca_cor, grupo_interseccional);

-- -----------------------------------------------------------------------------
-- 4. DIMENSÃO CONTEXTO DO CRIME (dim_contexto_crime)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_contexto_crime (
    id_contexto         SERIAL PRIMARY KEY,
    fonte_dados         VARCHAR(30) NOT NULL,      -- 'SINESP_MJSP' ou 'FOGO_CRUZADO'
    tipo_evento         VARCHAR(150) NOT NULL,     -- Feminicídio, Homicídio doloso, Ação policial, Disputa, etc.
    arma                VARCHAR(80) NOT NULL,      -- Arma de fogo, Arma branca, Outros / Não informado
    agente_seguranca    VARCHAR(80) NOT NULL,      -- Polícia Militar, Polícia Civil, Polícia Federal, Sem agente / Não aplicável
    acao_policial       BOOLEAN NOT NULL DEFAULT FALSE,
    presenca_agente     BOOLEAN NOT NULL DEFAULT FALSE,
    chacina             BOOLEAN NOT NULL DEFAULT FALSE,
    circunstancia       VARCHAR(100) NOT NULL DEFAULT 'Não especificada',
    local_ocorrencia    VARCHAR(100) NOT NULL DEFAULT 'Não especificado',
    UNIQUE (fonte_dados, tipo_evento, arma, agente_seguranca, acao_policial, presenca_agente, chacina, circunstancia, local_ocorrencia)
);

CREATE INDEX idx_dim_contexto_evento ON dim_contexto_crime (fonte_dados, tipo_evento);

-- -----------------------------------------------------------------------------
-- 5. TABELA FATO 1: VIOLÊNCIA NACIONAL SINESP/MJSP (fato_violencia_sinesp)
-- Base 1: fonte original.xlsx (Agregada por Município, Mês, Evento e Sexo)
-- -----------------------------------------------------------------------------
CREATE TABLE fato_violencia_sinesp (
    id_fato_sinesp      SERIAL PRIMARY KEY,
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

-- -----------------------------------------------------------------------------
-- 6. TABELA FATO 2: MICRODADOS INTERSECCIONAIS FOGO CRUZADO (fato_vitimas_fogo_cruzado)
-- Base 2: complemento fogo cruzado.xlsx (Anonimizada conforme LGPD)
-- -----------------------------------------------------------------------------
CREATE TABLE fato_vitimas_fogo_cruzado (
    id_fato_fc          SERIAL PRIMARY KEY,
    vitima_hash_lgpd    CHAR(16) NOT NULL,         -- Hash SHA-256 truncado (pseudonimização LGPD Art. 12/13)
    ocorrencia_hash     CHAR(16) NOT NULL,
    id_tempo            INTEGER NOT NULL REFERENCES dim_tempo(id_tempo),
    id_localidade       INTEGER NOT NULL REFERENCES dim_localidade(id_localidade),
    id_perfil           INTEGER NOT NULL REFERENCES dim_perfil_vitima(id_perfil),
    id_contexto         INTEGER NOT NULL REFERENCES dim_contexto_crime(id_contexto),
    situacao_vitima     VARCHAR(20) NOT NULL,      -- 'Morto' (Dead) ou 'Ferido' (Wounded)
    is_fatal            SMALLINT NOT NULL,         -- 1 se Morto, 0 se Ferido
    idade_vitima        SMALLINT,                  -- Idade em anos (NULL quando não informada)
    lat_aprox           NUMERIC(6, 2),             -- Latitude arredondada (2 casas = ~1.1 km para k-anonimato LGPD)
    lon_aprox           NUMERIC(6, 2)              -- Longitude arredondada (2 casas = ~1.1 km para k-anonimato LGPD)
);

CREATE INDEX idx_fato_fc_tempo_loc ON fato_vitimas_fogo_cruzado (id_tempo, id_localidade);
CREATE INDEX idx_fato_fc_perfil ON fato_vitimas_fogo_cruzado (id_perfil);
CREATE INDEX idx_fato_fc_contexto ON fato_vitimas_fogo_cruzado (id_contexto);

-- -----------------------------------------------------------------------------
-- 7. VIEWS ANALÍTICAS PARA O DASHBOARD (Regras de Negócio ODS 5 & ODS 18)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_resumo_interseccional_fogo_cruzado AS
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

CREATE OR REPLACE VIEW vw_resumo_violencia_sinesp AS
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

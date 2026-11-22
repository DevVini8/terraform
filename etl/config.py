"""
FASE 1, FASE 2 & FASE 3: Configurações centralizadas do Pipeline ETL, Segurança (.env),
Mapeamentos das 27 Capitais do Brasil e Critérios de Inclusão/Exclusão da Equipe.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env local (se existir)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Caminhos dos arquivos brutos e processados
RAW_SINESP_PATH = BASE_DIR / "fonte original.xlsx"
RAW_FOGO_CRUZADO_PATH = BASE_DIR / "complemento fogo cruzado.xlsx"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SCHEMA_SQL_PATH = BASE_DIR / "etl" / "schema.sql"
SQLITE_DB_PATH = PROCESSED_DIR / "dw_violencia_interseccional.db"
SQL_DUMP_PATH = PROCESSED_DIR / "dump_dw_violencia_interseccional.sql"

# Parâmetros de otimização de volume para respeitar o limite de 1 GB da Aiven (Fase 3)
CHUNK_SIZE = int(os.getenv("ETL_CHUNK_SIZE", "5000"))
MAX_DB_SIZE_MB = int(os.getenv("ETL_MAX_DB_SIZE_MB", "850"))
LGPD_HASH_SALT = os.getenv("LGPD_HASH_SALT", "ods5_ods18_lgpd_salt_2025")

# ==============================================================================
# CRITÉRIOS DE INCLUSÃO E EXCLUSÃO DEFINIDOS PELA EQUIPE
# ==============================================================================
# 1. Período temporal: Janeiro a Dezembro de 2025
ANO_REFERENCIA = 2025
MESES_INCLUSAO = list(range(1, 13))

# 2. Eventos na Fonte Original (SINESP): Estupro, Feminicídio e Tentativa de feminicídio
EVENTOS_INCLUSAO_SINESP = [
    "Estupro",
    "Feminicídio",
    "Tentativa de feminicídio",
]

# 3. Gêneros na Fonte Fogo Cruzado: Somente Mulher cis e Mulher trans e travesti
GENEROS_INCLUSAO_FC = [
    "Mulher cis",
    "Mulher trans e travesti",
]

# 4. Faixa etária na Fonte Fogo Cruzado: Mulheres entre 18 e 45 anos (excluindo sem idade informada)
IDADE_MIN_FC = 18
IDADE_MAX_FC = 45

# 5. Somente Capitais do Brasil (Mapeamento oficial UF -> Capital para validação estrita)
CAPITAIS_POR_UF = {
    "AC": "RIO BRANCO",
    "AL": "MACEIÓ",
    "AM": "MANAUS",
    "AP": "MACAPÁ",
    "BA": "SALVADOR",
    "CE": "FORTALEZA",
    "DF": "BRASÍLIA",
    "ES": "VITÓRIA",
    "GO": "GOIÂNIA",
    "MA": "SÃO LUÍS",
    "MG": "BELO HORIZONTE",
    "MS": "CAMPO GRANDE",
    "MT": "CUIABÁ",
    "PA": "BELÉM",
    "PB": "JOÃO PESSOA",
    "PE": "RECIFE",
    "PI": "TERESINA",
    "PR": "CURITIBA",
    "RJ": "RIO DE JANEIRO",
    "RN": "NATAL",
    "RO": "PORTO VELHO",
    "RR": "BOA VISTA",
    "RS": "PORTO ALEGRE",
    "SC": "FLORIANÓPOLIS",
    "SE": "ARACAJU",
    "SP": "SÃO PAULO",
    "TO": "PALMAS",
}

# Mapeamento oficial UF -> (Nome do Estado, Macrorregião IBGE)
UF_METADATA = {
    "AC": ("Acre", "Norte"),
    "AL": ("Alagoas", "Nordeste"),
    "AM": ("Amazonas", "Norte"),
    "AP": ("Amapá", "Norte"),
    "BA": ("Bahia", "Nordeste"),
    "CE": ("Ceará", "Nordeste"),
    "DF": ("Distrito Federal", "Centro-Oeste"),
    "ES": ("Espírito Santo", "Sudeste"),
    "GO": ("Goiás", "Centro-Oeste"),
    "MA": ("Maranhão", "Nordeste"),
    "MG": ("Minas Gerais", "Sudeste"),
    "MS": ("Mato Grosso do Sul", "Centro-Oeste"),
    "MT": ("Mato Grosso", "Centro-Oeste"),
    "PA": ("Pará", "Norte"),
    "PB": ("Paraíba", "Nordeste"),
    "PE": ("Pernambuco", "Nordeste"),
    "PI": ("Piauí", "Nordeste"),
    "PR": ("Paraná", "Sul"),
    "RJ": ("Rio de Janeiro", "Sudeste"),
    "RN": ("Rio Grande do Norte", "Nordeste"),
    "RO": ("Rondônia", "Norte"),
    "RR": ("Roraima", "Norte"),
    "RS": ("Rio Grande do Sul", "Sul"),
    "SC": ("Santa Catarina", "Sul"),
    "SE": ("Sergipe", "Nordeste"),
    "SP": ("São Paulo", "Sudeste"),
    "TO": ("Tocantins", "Norte"),
}

ESTADO_TO_UF = {
    "acre": "AC", "alagoas": "AL", "amazonas": "AM", "amapá": "AP", "amapa": "AP",
    "bahia": "BA", "ceará": "CE", "ceara": "CE", "distrito federal": "DF",
    "espírito santo": "ES", "espirito santo": "ES", "goiás": "GO", "goias": "GO",
    "maranhão": "MA", "maranhao": "MA", "minas gerais": "MG",
    "mato grosso do sul": "MS", "mato grosso": "MT", "pará": "PA", "para": "PA",
    "paraíba": "PB", "paraiba": "PB", "pernambuco": "PE", "piauí": "PI", "piaui": "PI",
    "paraná": "PR", "parana": "PR", "rio de janeiro": "RJ",
    "rio grande do norte": "RN", "rondônia": "RO", "rondonia": "RO",
    "roraima": "RR", "rio grande do sul": "RS", "santa catarina": "SC",
    "sergipe": "SE", "são paulo": "SP", "sao paulo": "SP", "tocantins": "TO",
}

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


def get_database_url() -> str:
    """
    Constrói ou retorna a URI de conexão com o banco PostgreSQL na Aiven
    a partir das variáveis de ambiente (.env ou GitHub Secrets).
    """
    direct_url = os.getenv("DATABASE_URL", "").strip()
    if direct_url and "seu-projeto" not in direct_url:
        if direct_url.startswith("postgres://"):
            direct_url = direct_url.replace("postgres://", "postgresql://", 1)
        return direct_url

    host = os.getenv("DB_HOST", "").strip()
    port = os.getenv("DB_PORT", "25060").strip()
    dbname = os.getenv("DB_NAME", "dw_violencia_interseccional").strip()
    user = os.getenv("DB_USER", "avnadmin").strip()
    password = os.getenv("DB_PASSWORD", "").strip()
    sslmode = os.getenv("DB_SSLMODE", "require").strip()

    if host and password and "seu-projeto" not in host:
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode={sslmode}"

    return ""

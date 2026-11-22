"""
FASE 3: Orquestrador Principal do Pipeline de ETL (pipeline.py)
Executa o fluxo completo:
  1. Extract (Leitura das bases SINESP e Instituto Fogo Cruzado)
  2. Transform (Data Wrangling, Anonimização LGPD, Amostragem/Otimização 1 GB e Modelagem Star Schema)
  3. Load (Exportação local + Carga em Batches no PostgreSQL Aiven)
"""
import argparse
import logging
import time

from etl.extract import extract_sinesp_dataset, extract_fogo_cruzado_dataset
from etl.transform import (
    clean_and_optimize_sinesp,
    clean_and_anonymize_fogo_cruzado,
    build_star_schema_tables,
)
from etl.load import (
    export_star_schema_locally,
    build_sqlite_warehouse_and_dump,
    load_to_aiven_postgres,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | [PIPELINE] %(message)s",
)
logger = logging.getLogger(__name__)


def run_pipeline(skip_db: bool = False, force_excel: bool = False) -> None:
    start_ts = time.time()
    logger.info("=" * 80)
    logger.info("INICIANDO PIPELINE ETL - BIG DATA & ANALYTICS (ODS 5 & ODS 18)")
    logger.info("=" * 80)

    # 1. EXTRACT
    df_sinesp_raw = extract_sinesp_dataset(use_cached_csv=not force_excel)
    df_fc_raw = extract_fogo_cruzado_dataset(use_cached_csv=not force_excel)

    # 2. TRANSFORM (Data Wrangling + LGPD + Otimização 1 GB + Star Schema)
    df_sinesp_clean = clean_and_optimize_sinesp(df_sinesp_raw)
    df_fc_clean = clean_and_anonymize_fogo_cruzado(df_fc_raw)
    star_tables = build_star_schema_tables(df_sinesp_clean, df_fc_clean)

    # Salva também os datasets tratados consolidados para leitura instantânea pelo Dashboard
    from etl.config import PROCESSED_DIR
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_sinesp_clean.to_csv(PROCESSED_DIR / "sinesp_tratado.csv", index=False, encoding="utf-8")
    df_fc_clean.to_csv(PROCESSED_DIR / "fogo_cruzado_tratado.csv", index=False, encoding="utf-8")

    # 3. LOAD (Local Cache CSV + Banco Relacional SQLite & Dump SQL + Aiven PostgreSQL)
    export_star_schema_locally(star_tables)
    build_sqlite_warehouse_and_dump(star_tables)
    if not skip_db:
        load_to_aiven_postgres(star_tables)

    elapsed = round(time.time() - start_ts, 2)
    logger.info("=" * 80)
    logger.info(f"PIPELINE ETL CONCLUÍDO COM SUCESSO EM {elapsed}s!")
    logger.info("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ETL - Violência Interseccional ODS 5 & ODS 18")
    parser.add_argument("--skip-db", action="store_true", help="Apenas processa e gera as tabelas locais sem conectar ao PostgreSQL")
    parser.add_argument("--force-excel", action="store_true", help="Força a releitura direta dos arquivos .xlsx brutos")
    args = parser.parse_args()
    run_pipeline(skip_db=args.skip_db, force_excel=args.force_excel)

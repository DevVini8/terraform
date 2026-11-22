"""
FASE 5: Validação de Reprodutibilidade e Testes Automatizados (test_business_rules_and_lgpd.py)
Valida todos os Critérios de Inclusão e Exclusão definidos pela equipe:
  1. Período: Janeiro a Dezembro de 2025
  2. Geografia: Somente Capitais do Brasil (e exclusão de dados sem município identificado)
  3. SINESP: Eventos de Estupro, Feminicídio e Tentativa de feminicídio + Somente vítimas do sexo feminino
  4. Fogo Cruzado: Somente Mulher cis e Mulher trans e travesti (exclusão de sem gênero informado e homens)
  5. Fogo Cruzado: Somente Mulheres entre 18 e 45 anos (exclusão de sem idade informada)
  6. Conformidade LGPD (remoção de PII, hash SHA-256 e truncamento de coordenadas)
"""
import unittest
import numpy as np
import pandas as pd

from etl.transform import (
    pseudonymize_id_lgpd,
    clean_and_optimize_sinesp,
    clean_and_anonymize_fogo_cruzado,
    build_star_schema_tables,
)
from dashboard.business_rules import (
    compute_kpi_metrics,
    build_intersectional_matrix,
)


class TestTeamCriteriaAndLGPD(unittest.TestCase):
    def setUp(self):
        self.sample_sinesp = pd.DataFrame([
            # 1. VÁLIDO: Capital (Salvador-BA), 2025, Feminicídio, vítimas feminino = 4
            {
                "uf": "BA", "municipio": "SALVADOR", "evento": "Feminicídio",
                "data_referencia": "2025-03-01", "agente": "Não informado",
                "arma": "Arma de fogo", "faixa_etaria": "Adulto",
                "feminino": 4, "masculino": 0, "nao_informado": 0,
                "total_vitima": 4, "total": 4, "total_peso": 4.0, "abrangencia": "Estadual",
            },
            # 2. VÁLIDO: Capital (Salvador-BA), 2025, Tentativa de feminicídio, vítimas feminino = 6
            {
                "uf": "BA", "municipio": "SALVADOR", "evento": "Tentativa de feminicídio",
                "data_referencia": "2025-04-01", "agente": "Não informado",
                "arma": "Arma branca", "faixa_etaria": "Adulto",
                "feminino": 6, "masculino": 1, "nao_informado": 0,
                "total_vitima": 7, "total": 7, "total_peso": 7.0, "abrangencia": "Estadual",
            },
            # 3. EXCLUÍDO (Município do interior - não é capital): Feira de Santana-BA
            {
                "uf": "BA", "municipio": "FEIRA DE SANTANA", "evento": "Feminicídio",
                "data_referencia": "2025-03-01", "agente": "Não informado",
                "arma": "Arma de fogo", "faixa_etaria": "Adulto",
                "feminino": 2, "masculino": 0, "nao_informado": 0,
                "total_vitima": 2, "total": 2, "total_peso": 2.0, "abrangencia": "Estadual",
            },
            # 4. EXCLUÍDO (Sem município identificado): Estupro agregado estadual sem município
            {
                "uf": "BA", "municipio": "", "evento": "Estupro",
                "data_referencia": "2025-03-01", "agente": "Não informado",
                "arma": "Não informada", "faixa_etaria": "Adulto",
                "feminino": 50, "masculino": 5, "nao_informado": 0,
                "total_vitima": 55, "total": 55, "total_peso": 55.0, "abrangencia": "Estadual",
            },
            # 5. EXCLUÍDO (Evento fora do escopo): Furto de veículo
            {
                "uf": "BA", "municipio": "SALVADOR", "evento": "Furto de veículo",
                "data_referencia": "2025-03-01", "agente": "Não informado",
                "arma": "Não informada", "faixa_etaria": "Adulto",
                "feminino": 10, "masculino": 20, "nao_informado": 0,
                "total_vitima": 30, "total": 30, "total_peso": 30.0, "abrangencia": "Estadual",
            },
        ])

        self.sample_fc = pd.DataFrame([
            # 1. VÁLIDO: 2025, Capital (Salvador), Mulher cis, 24 anos (entre 18 e 45), Negra
            {
                "estado": "Bahia", "cidade": "Salvador", "bairro": "LIBERDADE",
                "ocorrencia_id": "4562fbcf-4a87-4185-ad27-87c308490351",
                "ocorrencia_numero": 50480, "data": "2025-02-10",
                "endereco": "Rua Valê do Queimadinho, 123 - Salvador",
                "latitude": -129586607, "longitude": -384983746,
                "acao_policial": 1, "presenca_agente": 1,
                "motivo_principal": "Ação policial", "chacina": 0,
                "vitima_id": "ce4fa168-9551-4e8b-8154-8dd429c4418a",
                "situacao": "Dead", "circunstancias": "Bala perdida",
                "tipo_pessoa": "Civilian", "idade": 24, "faixa_etaria": "Adulto",
                "genero": "Mulher cis", "raca": "Negra", "local": "Via pública",
                "cargo_agente": "Soldado", "unidade": "BPM",
            },
            # 2. VÁLIDO: 2025, Capital (Recife), Mulher trans e travesti, 36 anos (entre 18 e 45), Negra
            {
                "estado": "Pernambuco", "cidade": "Recife", "bairro": "BOA VIAGEM",
                "ocorrencia_id": "a3f252a9-11d8-4cc0-a1b3-e09af6e8d377",
                "ocorrencia_numero": 50481, "data": "2025-05-15",
                "endereco": "Av. Conselheiro Aguiar, 500",
                "latitude": -8.1189, "longitude": -34.9012,
                "acao_policial": 0, "presenca_agente": 0,
                "motivo_principal": "Homicidio/Tentativa", "chacina": 0,
                "vitima_id": "92a23568-c7a7-4a3f-83c4-33776be08fb8",
                "situacao": "Wounded", "circunstancias": "Sem identificação",
                "tipo_pessoa": "Civilian", "idade": 36, "faixa_etaria": "Adulto",
                "genero": "Mulher trans e travesti", "raca": "Negra", "local": "Via pública",
                "cargo_agente": "Não se aplica", "unidade": "Não se aplica",
            },
            # 3. EXCLUÍDO (Sem idade informada): Mulher cis em Salvador em 2025 com idade NaN
            {
                "estado": "Bahia", "cidade": "Salvador", "bairro": "BROTAS",
                "ocorrencia_id": "b1111111-11d8-4cc0-a1b3-e09af6e8d377",
                "ocorrencia_numero": 50482, "data": "2025-06-10",
                "endereco": "Rua X", "latitude": -12.98, "longitude": -38.48,
                "acao_policial": 0, "presenca_agente": 0,
                "motivo_principal": "Homicidio/Tentativa", "chacina": 0,
                "vitima_id": "c1111111-c7a7-4a3f-83c4-33776be08fb8",
                "situacao": "Dead", "circunstancias": "Sem identificação",
                "tipo_pessoa": "Civilian", "idade": np.nan, "faixa_etaria": "Adulto",
                "genero": "Mulher cis", "raca": "Negra", "local": "Via pública",
                "cargo_agente": "", "unidade": "",
            },
            # 4. EXCLUÍDO (Idade fora de 18-45 anos): Mulher cis de 55 anos
            {
                "estado": "Rio de Janeiro", "cidade": "Rio de Janeiro", "bairro": "COPACABANA",
                "ocorrencia_id": "b2222222-11d8-4cc0-a1b3-e09af6e8d377",
                "ocorrencia_numero": 50483, "data": "2025-07-10",
                "endereco": "Rua Y", "latitude": -22.97, "longitude": -43.18,
                "acao_policial": 0, "presenca_agente": 0,
                "motivo_principal": "Homicidio/Tentativa", "chacina": 0,
                "vitima_id": "c2222222-c7a7-4a3f-83c4-33776be08fb8",
                "situacao": "Wounded", "circunstancias": "Sem identificação",
                "tipo_pessoa": "Civilian", "idade": 55, "faixa_etaria": "Adulto",
                "genero": "Mulher cis", "raca": "Branca", "local": "Via pública",
                "cargo_agente": "", "unidade": "",
            },
            # 5. EXCLUÍDO (Gênero Homem cis / Sem gênero informado): Homem cis de 25 anos
            {
                "estado": "Rio de Janeiro", "cidade": "Rio de Janeiro", "bairro": "MARÉ",
                "ocorrencia_id": "b3333333-11d8-4cc0-a1b3-e09af6e8d377",
                "ocorrencia_numero": 50484, "data": "2025-08-10",
                "endereco": "Rua Z", "latitude": -22.85, "longitude": -43.24,
                "acao_policial": 1, "presenca_agente": 1,
                "motivo_principal": "Ação policial", "chacina": 0,
                "vitima_id": "c3333333-c7a7-4a3f-83c4-33776be08fb8",
                "situacao": "Dead", "circunstancias": "Sem identificação",
                "tipo_pessoa": "Civilian", "idade": 25, "faixa_etaria": "Adulto",
                "genero": "Homem cis", "raca": "Negra", "local": "Via pública",
                "cargo_agente": "", "unidade": "",
            },
            # 6. EXCLUÍDO (Município não é capital): Belford Roxo-RJ
            {
                "estado": "Rio de Janeiro", "cidade": "Belford Roxo", "bairro": "CENTRO",
                "ocorrencia_id": "b4444444-11d8-4cc0-a1b3-e09af6e8d377",
                "ocorrencia_numero": 50485, "data": "2025-09-10",
                "endereco": "Rua W", "latitude": -22.76, "longitude": -43.39,
                "acao_policial": 0, "presenca_agente": 0,
                "motivo_principal": "Homicidio/Tentativa", "chacina": 0,
                "vitima_id": "c4444444-c7a7-4a3f-83c4-33776be08fb8",
                "situacao": "Dead", "circunstancias": "Sem identificação",
                "tipo_pessoa": "Civilian", "idade": 28, "faixa_etaria": "Adulto",
                "genero": "Mulher cis", "raca": "Negra", "local": "Via pública",
                "cargo_agente": "", "unidade": "",
            },
        ])

    def test_sinesp_inclusion_and_exclusion_criteria(self):
        df_sin = clean_and_optimize_sinesp(self.sample_sinesp, strict_exclude_unidentified_municipality=True)
        # Apenas as 2 linhas de Salvador (Feminicídio e Tentativa de feminicídio) devem permanecer
        self.assertEqual(len(df_sin), 2)
        self.assertEqual(df_sin["feminino"].sum(), 10)
        # Vítimas masculinas devem ser zeradas pois o critério inclui somente vítimas do sexo feminino
        self.assertEqual(df_sin["masculino"].sum(), 0)
        self.assertEqual(df_sin["total_vitima"].sum(), 10)

    def test_fogo_cruzado_inclusion_exclusion_and_lgpd(self):
        df_fc = clean_and_anonymize_fogo_cruzado(self.sample_fc)
        # Apenas as 2 primeiras linhas (Mulher cis 24a em Salvador e Mulher trans 36a em Recife, em 2025) devem permanecer
        self.assertEqual(len(df_fc), 2)
        self.assertTrue(df_fc["idade"].between(18, 45).all())
        self.assertTrue(df_fc["genero"].isin(["Mulher cis", "Mulher trans e travesti"]).all())
        for pii_col in ["endereco", "cargo_agente", "unidade", "vitima_id", "ocorrencia_id"]:
            self.assertNotIn(pii_col, df_fc.columns)
        self.assertEqual(df_fc.iloc[0]["lat_aprox"], -12.96)

    def test_kpis_and_star_schema_on_filtered_cohort(self):
        df_sin = clean_and_optimize_sinesp(self.sample_sinesp)
        df_fc = clean_and_anonymize_fogo_cruzado(self.sample_fc)
        tables = build_star_schema_tables(df_sin, df_fc)
        self.assertEqual(len(tables["fato_violencia_sinesp"]), 2)
        self.assertEqual(len(tables["fato_vitimas_fogo_cruzado"]), 2)

        kpis = compute_kpi_metrics(df_sin, df_fc, stat_mode="Média")
        self.assertEqual(kpis["total_fem_sinesp"], 10)
        self.assertEqual(kpis["taxa_letalidade_feminicidio_pct"], 40.0)
        self.assertEqual(kpis["total_mulheres_fc"], 2)
        self.assertEqual(kpis["idade_central"], 30.0)


if __name__ == "__main__":
    unittest.main()

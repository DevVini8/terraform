"""
Dashboard Interativo Simplificado — Apresentação em Sala
Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)
Alinhado à ODS 5 (Igualdade de Gênero) e à ODS 18 (Igualdade Étnico-Racial).
"""
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from etl.config import (
    RAW_SINESP_PATH,
    RAW_FOGO_CRUZADO_PATH,
    MESES_PT,
)
from etl.extract import extract_sinesp_dataset, extract_fogo_cruzado_dataset
from etl.transform import (
    clean_and_optimize_sinesp,
    clean_and_anonymize_fogo_cruzado,
)
from dashboard.business_rules import (
    compute_kpi_metrics,
    build_intersectional_matrix,
    compute_dynamic_aggregation_by_capital,
)

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Violência contra a Mulher nas Capitais (2025)",
    page_icon="📊",
    layout="wide",
)


@st.cache_data(ttl=3600)
def carregar_dados():
    sinesp_raw = extract_sinesp_dataset(RAW_SINESP_PATH, use_cached_csv=True)
    fc_raw = extract_fogo_cruzado_dataset(RAW_FOGO_CRUZADO_PATH, use_cached_csv=True)

    df_sinesp = clean_and_optimize_sinesp(sinesp_raw, strict_exclude_unidentified_municipality=True)
    df_fc = clean_and_anonymize_fogo_cruzado(fc_raw)
    return df_sinesp, df_fc


df_sinesp_full, df_fc_full = carregar_dados()

# ==============================================================================
# BARRA LATERAL: FILTROS SIMPLES E DIRETOS
# ==============================================================================
st.sidebar.header("🎛️ Filtros da Apresentação")

# 1. Alternador Média vs. Mediana
stat_mode = st.sidebar.radio(
    "Medida Estatística:",
    options=["Média", "Mediana"],
    horizontal=True,
)

# 2. Filtro de Região
regioes_disp = sorted(df_sinesp_full["regiao"].unique().tolist())
regioes_sel = st.sidebar.multiselect(
    "Região:",
    options=regioes_disp,
    default=regioes_disp,
) or regioes_disp

# 3. Filtro de Capital
capitais_disp = sorted(
    df_sinesp_full[df_sinesp_full["regiao"].isin(regioes_sel)]["municipio"].unique().tolist()
)
capitais_sel = st.sidebar.multiselect(
    "Capital:",
    options=capitais_disp,
    default=capitais_disp,
) or capitais_disp

# 4. Filtro de Mês (2025)
meses_disp = sorted(df_sinesp_full["mes"].unique().tolist())
meses_opcoes = [f"{m:02d} - {MESES_PT[m]}" for m in meses_disp]
meses_sel_lbl = st.sidebar.multiselect(
    "Mês de 2025:",
    options=meses_opcoes,
    default=meses_opcoes,
) or meses_opcoes
meses_sel = [int(x.split(" - ")[0]) for x in meses_sel_lbl]

st.sidebar.divider()
st.sidebar.subheader("🧬 Filtros Fogo Cruzado (ODS 5 & 18)")

# 5. Filtro de Gênero (Mulher cis / Mulher trans e travesti)
generos_disp = sorted(df_fc_full["genero"].unique().tolist())
generos_sel = st.sidebar.multiselect(
    "Gênero:",
    options=generos_disp,
    default=generos_disp,
) or generos_disp

# 6. Filtro de Raça/Cor
racas_disp = sorted(df_fc_full["raca"].unique().tolist())
racas_sel = st.sidebar.multiselect(
    "Raça/Cor:",
    options=racas_disp,
    default=racas_disp,
) or racas_disp

# 7. Filtro de Idade (18 a 45 anos)
idade_range = st.sidebar.slider(
    "Faixa de Idade (18 a 45 anos):",
    min_value=18,
    max_value=45,
    value=(18, 45),
)

# Aplicação dos filtros
df_sinesp = df_sinesp_full[
    (df_sinesp_full["regiao"].isin(regioes_sel))
    & (df_sinesp_full["municipio"].isin(capitais_sel))
    & (df_sinesp_full["mes"].isin(meses_sel))
].copy()

caps_fc = [c for c in capitais_sel if c in df_fc_full["cidade"].unique()] or df_fc_full["cidade"].unique().tolist()
df_fc = df_fc_full[
    (df_fc_full["cidade"].isin(caps_fc))
    & (df_fc_full["mes"].isin(meses_sel))
    & (df_fc_full["genero"].isin(generos_sel))
    & (df_fc_full["raca"].isin(racas_sel))
    & (df_fc_full["idade"].between(idade_range[0], idade_range[1]))
].copy()

# ==============================================================================
# TÍTULO E 4 INDICADORES PRINCIPAIS (KPIs)
# ==============================================================================
st.title("📊 Violência contra a Mulher nas Capitais do Brasil (2025)")
st.caption("ODS 5 (Igualdade de Gênero) & ODS 18 (Igualdade Étnico-Racial) • Fontes: SINESP/MJSP e Instituto Fogo Cruzado")

kpis = compute_kpi_metrics(df_sinesp, df_fc, stat_mode=stat_mode)

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Vítimas Femininas nas Capitais (SINESP)",
    f"{kpis['total_fem_sinesp']:,}".replace(",", "."),
    f"{kpis['vit_feminicidio']} Feminicídios | {kpis['vit_tentativa']} Tentativas",
)
c2.metric(
    "Mulheres Baleadas 18–45a (Fogo Cruzado)",
    f"{kpis['total_mulheres_fc']}",
    f"{kpis['mulheres_cis_fc']} Mulheres cis | {kpis['mulheres_trans_fc']} Trans/Travestis",
)
c3.metric(
    "Letalidade Armada (Fogo Cruzado)",
    f"{kpis['taxa_letalidade_fc']}%",
    f"{kpis['mortas_fc']} Mortas e {kpis['feridas_fc']} Feridas",
)
c4.metric(
    f"Mulheres Negras & Idade ({stat_mode})",
    f"{kpis['pct_negras_identificadas']}% Negras",
    f"{stat_mode} de Idade: {kpis['idade_central']} anos",
)

st.divider()

# ==============================================================================
# 2 ABAS SIMPLES E DIRETAS PARA APRESENTAÇÃO
# ==============================================================================
tab1, tab2 = st.tabs([
    "🚺 1. Capitais do Brasil (SINESP 2025)",
    "🧬 2. Gênero, Raça e Idade (Fogo Cruzado 2025)",
])

# ------------------------------------------------------------------------------
# ABA 1: SINESP (27 CAPITAIS EM 2025)
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Violência contra a Mulher nas Capitais (SINESP 2025)")

    if len(df_sinesp) > 0:
        cap_summary = compute_dynamic_aggregation_by_capital(df_sinesp, stat_mode=stat_mode)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_cap = px.bar(
                cap_summary.head(12),
                x="municipio",
                y=["Feminicídio", "Tentativa de feminicídio"],
                barmode="stack",
                text_auto=True,
                title="Top 12 Capitais com Mais Vítimas Femininas (2025)",
                labels={"value": "Vítimas", "municipio": "Capital", "variable": "Crime"},
                color_discrete_map={"Feminicídio": "#dc2626", "Tentativa de feminicídio": "#fb923c"},
            )
            st.plotly_chart(fig_cap, use_container_width=True)

        with col_g2:
            mensal = (
                df_sinesp.groupby(["mes", "nome_mes", "evento"], as_index=False)
                .agg(vitimas=("feminino", "sum"))
                .sort_values("mes")
            )
            fig_mes = px.line(
                mensal,
                x="nome_mes",
                y="vitimas",
                color="evento",
                markers=True,
                title="Evolução Mensal nas Capitais (Jan a Dez 2025)",
                labels={"nome_mes": "Mês", "vitimas": "Vítimas Femininas", "evento": "Crime"},
                color_discrete_map={"Feminicídio": "#dc2626", "Tentativa de feminicídio": "#fb923c"},
            )
            st.plotly_chart(fig_mes, use_container_width=True)

        st.markdown(f"**Resumo por Capital (`{stat_mode}` Mensal e Total em 2025)**")
        st.dataframe(
            cap_summary[[
                "regiao", "uf", "municipio", "Feminicídio",
                "Tentativa de feminicídio", "soma_vitimas_fem", "metrica_central_mensal",
            ]].rename(columns={
                "regiao": "Região",
                "uf": "UF",
                "municipio": "Capital",
                "soma_vitimas_fem": "Total Vítimas (2025)",
                "metrica_central_mensal": f"{stat_mode} Mensal",
            }),
            use_container_width=True,
        )
    else:
        st.info("Sem dados para os filtros selecionados.")

# ------------------------------------------------------------------------------
# ABA 2: FOGO CRUZADO (INTERSECCIONALIDADE ODS 5 & ODS 18)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Mulheres Baleadas (18 a 45 anos) por Gênero e Raça/Cor (Fogo Cruzado 2025)")

    if len(df_fc) > 0:
        matrix_df = build_intersectional_matrix(df_fc)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fig_raca = px.bar(
                matrix_df,
                x="raca",
                y="total_vitimas",
                color="genero",
                barmode="group",
                text_auto=True,
                title="Mulheres Baleadas por Raça/Cor (ODS 18) e Gênero (ODS 5)",
                labels={"raca": "Raça/Cor", "total_vitimas": "Total de Mulheres", "genero": "Gênero"},
                color_discrete_map={"Mulher cis": "#e11d48", "Mulher trans e travesti": "#7c3aed"},
            )
            st.plotly_chart(fig_raca, use_container_width=True)

        with col_f2:
            por_cap = (
                df_fc.groupby(["cidade", "situacao"], as_index=False)
                .agg(vitimas=("is_fatal", "count"))
            )
            fig_sit = px.bar(
                por_cap,
                x="cidade",
                y="vitimas",
                color="situacao",
                barmode="group",
                text_auto=True,
                title="Mulheres Mortas vs. Feridas por Capital (2025)",
                labels={"cidade": "Capital", "vitimas": "Mulheres", "situacao": "Situação"},
                color_discrete_map={"Morto": "#dc2626", "Ferido": "#f59e0b"},
            )
            st.plotly_chart(fig_sit, use_container_width=True)

        st.markdown("**Tabela Resumo: Cruzamento Gênero × Raça/Cor**")
        st.dataframe(
            matrix_df[[
                "genero", "raca", "total_vitimas", "total_mortos",
                "total_feridos", "taxa_letalidade_pct", "idade_media", "idade_mediana",
            ]].rename(columns={
                "genero": "Gênero",
                "raca": "Raça/Cor",
                "total_vitimas": "Total Vítimas",
                "total_mortos": "Mortas",
                "total_feridos": "Feridas",
                "taxa_letalidade_pct": "Letalidade (%)",
                "idade_media": "Idade Média",
                "idade_mediana": "Idade Mediana",
            }),
            use_container_width=True,
        )
    else:
        st.info("Sem dados para os filtros selecionados.")


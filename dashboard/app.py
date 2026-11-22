"""
FASE 4 & FASE 5: Dashboard Interativo de Business Intelligence (Streamlit)
Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)
Alinhado à ODS 5 (Igualdade de Gênero) e à ODS 18 (Igualdade Étnico-Racial).

Recorte Metodológico Estrito da Equipe:
  • Critérios de Inclusão:
      - Janeiro a Dezembro de 2025
      - Somente Capitais do Brasil
      - Fonte Original (SINESP): Eventos de Estupro, Feminicídio e Tentativa de feminicídio
      - Fonte Original (SINESP): Somente vítimas do sexo feminino
      - Fonte Fogo Cruzado: Mulheres entre 18 e 45 anos
      - Fonte Fogo Cruzado: Somente gênero Mulher cis e Mulher trans e travesti
  • Critérios de Exclusão:
      - Dados sem gênero informado no Fogo Cruzado
      - Dados sem município identificado
      - Dados sem idade informada no Fogo Cruzado
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from etl.config import (
    PROCESSED_DIR,
    RAW_SINESP_PATH,
    RAW_FOGO_CRUZADO_PATH,
    SQLITE_DB_PATH,
    SQL_DUMP_PATH,
    SCHEMA_SQL_PATH,
    UF_METADATA,
    MESES_PT,
    CAPITAIS_POR_UF,
    get_database_url,
)
from etl.extract import extract_sinesp_dataset, extract_fogo_cruzado_dataset
from etl.transform import clean_and_optimize_sinesp, clean_and_anonymize_fogo_cruzado, build_star_schema_tables
from etl.load import build_sqlite_warehouse_and_dump
from dashboard.business_rules import (
    compute_kpi_metrics,
    build_intersectional_matrix,
    compute_dynamic_aggregation_by_capital,
)

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Observatório Interseccional das Capitais (2025) | ODS 5 & ODS 18",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.3rem; padding-bottom: 2rem; }
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.18);
    }
    .ods-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-right: 8px;
    }
    .ods5 { background-color: #ff3a21; color: white; }
    .ods18 { background-color: #7c3aed; color: white; }
    .lgpd { background-color: #059669; color: white; }
    .criteria { background-color: #1d4ed8; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# CARREGAMENTO DE DADOS COM OS CRITÉRIOS DE INCLUSÃO E EXCLUSÃO DA EQUIPE
# ==============================================================================
@st.cache_data(ttl=3600, show_spinner="Aplicando Critérios de Inclusão e Exclusão da Equipe (Capitais 2025)...")
def load_team_cohort_datasets(strict_exclude_unidentified_mun: bool = True):
    """
    Carrega as duas bases aplicando estritamente os Critérios de Inclusão e Exclusão da Equipe.
    """
    source_status = "Pipeline ETL • Recorte Capitais 2025"

    # Carrega a partir do CSV pré-processado ou lê as planilhas brutas e aplica os filtros da equipe
    sinesp_raw = extract_sinesp_dataset(RAW_SINESP_PATH, use_cached_csv=True)
    fc_raw = extract_fogo_cruzado_dataset(RAW_FOGO_CRUZADO_PATH, use_cached_csv=True)

    df_sinesp = clean_and_optimize_sinesp(
        sinesp_raw,
        strict_exclude_unidentified_municipality=strict_exclude_unidentified_mun,
    )
    df_fc = clean_and_anonymize_fogo_cruzado(fc_raw)

    return df_sinesp, df_fc, source_status


# ==============================================================================
# BARRA LATERAL: CRITÉRIOS DA EQUIPE, ALTERNADORES E FILTROS CRUZADOS (FASE 4)
# ==============================================================================
st.sidebar.header("🎛️ Painel de Controle & Filtros")

st.sidebar.subheader("⚡ Alternadores Dinâmicos (Fase 4)")
stat_mode = st.sidebar.radio(
    "Medida de Tendência Central:",
    options=["Média", "Mediana"],
    index=0,
    horizontal=True,
    help="Alterna dinamicamente entre Média e Mediana para a idade das vítimas (18–45 anos) e vítimas mensais por Capital.",
)

scale_mode = st.sidebar.radio(
    "Escala de Visualização:",
    options=["Valores Absolutos", "Proporção Relativa (%)"],
    index=0,
    horizontal=True,
    help="Alterna gráficos entre número absoluto de vítimas femininas e proporção percentual (%).",
)

st.sidebar.divider()
st.sidebar.subheader("📌 Regra sobre Município no SINESP")
strict_mun_toggle = st.sidebar.checkbox(
    "Exclusão Estrita: Sem Município Identificado",
    value=True,
    help=(
        "Na fonte original (SINESP), Feminicídio e Tentativa de feminicídio possuem o município da Capital identificado. "
        "Já os 324 registros de Estupro estão agregados por UF com a coluna município em branco. "
        "Desmarque caso deseje visualizar também Estupro alocado à respectiva Capital/UF."
    ),
)

df_sinesp_full, df_fc_full, data_source_label = load_team_cohort_datasets(
    strict_exclude_unidentified_mun=strict_mun_toggle
)

st.sidebar.divider()
st.sidebar.subheader("🌍 Filtros Cruzados (Capitais 2025)")

# 1. Filtro de Mês (Janeiro a Dezembro de 2025)
meses_disp = sorted(list(set(df_sinesp_full["mes"].unique().tolist()) | set(df_fc_full["mes"].unique().tolist())))
meses_nomes_map = {m: f"{m:02d} - {MESES_PT.get(m, str(m))}" for m in meses_disp}
meses_sel_labels = st.sidebar.multiselect(
    "Meses de 2025 (Jan–Dez):",
    options=[meses_nomes_map[m] for m in meses_disp],
    default=[meses_nomes_map[m] for m in meses_disp],
)
meses_sel = [int(lbl.split(" - ")[0]) for lbl in meses_sel_labels] if meses_sel_labels else meses_disp

# 2. Filtro de Região
regioes_disp = sorted(
    list(set(df_sinesp_full["regiao"].unique().tolist()) | set(df_fc_full["regiao"].unique().tolist()))
)
regioes_sel = st.sidebar.multiselect(
    "Macrorregião:",
    options=regioes_disp,
    default=regioes_disp,
)
if not regioes_sel:
    regioes_sel = regioes_disp

# 3. Filtro de Capital / UF
capitais_disp = sorted(
    df_sinesp_full[df_sinesp_full["regiao"].isin(regioes_sel)]["municipio"].unique().tolist()
)
capitais_sel = st.sidebar.multiselect(
    "Capitais do Brasil (SINESP / Fogo Cruzado):",
    options=capitais_disp,
    default=capitais_disp,
)
if not capitais_sel:
    capitais_sel = capitais_disp

st.sidebar.divider()
st.sidebar.subheader("🧬 Filtros Interseccionais (ODS 5 & 18)")

# 4. Filtro de Identidade de Gênero (Somente Mulher cis e Mulher trans e travesti)
generos_fc_disp = sorted(df_fc_full["genero"].unique().tolist())
generos_sel = st.sidebar.multiselect(
    "Gênero (Fogo Cruzado):",
    options=generos_fc_disp,
    default=generos_fc_disp,
)
if not generos_sel:
    generos_sel = generos_fc_disp

# 5. Filtro de Raça/Cor (ODS 18)
racas_fc_disp = sorted(df_fc_full["raca"].unique().tolist())
racas_sel = st.sidebar.multiselect(
    "Raça / Cor (ODS 18 - Fogo Cruzado):",
    options=racas_fc_disp,
    default=racas_fc_disp,
)
if not racas_sel:
    racas_sel = racas_fc_disp

# 6. Filtro de Faixa de Idade dentro do intervalo 18 a 45 anos
idade_range = st.sidebar.slider(
    "Faixa Etária de Inclusão (18 a 45 anos):",
    min_value=18,
    max_value=45,
    value=(18, 45),
)

# Aplicação dos filtros cruzados
df_sinesp = df_sinesp_full[
    (df_sinesp_full["mes"].isin(meses_sel))
    & (df_sinesp_full["regiao"].isin(regioes_sel))
    & (df_sinesp_full["municipio"].isin(capitais_sel))
].copy()

caps_fc_validas = [c for c in capitais_sel if c in df_fc_full["cidade"].unique()]
if not caps_fc_validas:
    caps_fc_validas = df_fc_full["cidade"].unique().tolist()

df_fc = df_fc_full[
    (df_fc_full["mes"].isin(meses_sel))
    & (df_fc_full["cidade"].isin(caps_fc_validas))
    & (df_fc_full["genero"].isin(generos_sel))
    & (df_fc_full["raca"].isin(racas_sel))
    & (df_fc_full["idade"].between(idade_range[0], idade_range[1]))
].copy()

# ==============================================================================
# CABEÇALHO E RESUMO DOS CRITÉRIOS DA EQUIPE
# ==============================================================================
st.markdown(
    """
    <div>
        <span class="ods-badge ods5">ODS 5 • Igualdade de Gênero</span>
        <span class="ods-badge ods18">ODS 18 • Igualdade Étnico-Racial</span>
        <span class="ods-badge criteria">Recorte 2025 • Somente Capitais • Mulheres (18–45 anos)</span>
        <span class="ods-badge lgpd">Conformidade LGPD • Anonimizado</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.title("📊 Observatório Interseccional da Violência contra a Mulher nas Capitais (2025)")

with st.expander("📋 Ver Critérios de Inclusão e Exclusão Aplicados pela Equipe", expanded=False):
    c_inc, c_exc = st.columns(2)
    with c_inc:
        st.markdown(
            "**✅ Critérios de Inclusão Ativos:**\n"
            "- **Período:** Janeiro a Dezembro de 2025 (`01/2025` a `12/2025`)\n"
            "- **Geografia:** Somente **Capitais do Brasil** (27 capitais no SINESP; Salvador, Recife, Rio de Janeiro e Belém no Fogo Cruzado)\n"
            "- **Eventos (Fonte Original - SINESP):** `Estupro`, `Feminicídio` e `Tentativa de feminicídio`\n"
            "- **Sexo (Fonte Original - SINESP):** Somente vítimas do **sexo feminino**\n"
            "- **Idade (Fogo Cruzado):** Mulheres entre **18 e 45 anos**\n"
            "- **Gênero (Fogo Cruzado):** Somente `Mulher cis` e `Mulher trans e travesti`"
        )
    with c_exc:
        st.markdown(
            "**🚫 Critérios de Exclusão Aplicados:**\n"
            "- **Sem Gênero Informado (Fogo Cruzado):** Excluídos `1.240` registros sem gênero e `40.560` registros masculinos\n"
            "- **Sem Município Identificado:** Excluídos registros sem município identificado ou fora das Capitais (no SINESP, os `324` registros estaduais de *Estupro* possuem o campo `municipio` em branco na fonte original)\n"
            "- **Sem Idade Informada (Fogo Cruzado):** Excluídos `96` registros de mulheres nas capitais em 2025 sem idade preenchida e `50` fora da faixa 18–45 anos"
        )

# ==============================================================================
# SEÇÃO SUPERIOR: 6 MÉTRICAS ANALÍTICAS CHAVE (KPIs - FASE 4)
# ==============================================================================
kpis = compute_kpi_metrics(df_sinesp, df_fc, stat_mode=stat_mode)

col_k1, col_k2, col_k3, col_k4, col_k5, col_k6 = st.columns(6)

with col_k1:
    st.metric(
        label="Vítimas Femininas (Capitais SINESP)",
        value=f"{kpis['total_fem_sinesp']:,}".replace(",", "."),
        delta=f"{kpis['vit_por_capital']} vítimas/capital ({stat_mode})",
    )

with col_k2:
    st.metric(
        label="Feminicídios Consumados (Capitais)",
        value=f"{kpis['vit_feminicidio']:,}".replace(",", "."),
        delta=f"{kpis['taxa_letalidade_feminicidio_pct']}% de letalidade sobre tentativas",
    )

with col_k3:
    st.metric(
        label="Tentativas de Feminicídio (Capitais)",
        value=f"{kpis['vit_tentativa']:,}".replace(",", "."),
        delta=(
            f"Estupros (UF): {kpis['vit_estupro']:,}".replace(",", ".")
            if kpis["vit_estupro"] > 0
            else f"Em {kpis['capitais_ativas_sinesp']} Capitais brasileiras"
        ),
    )

with col_k4:
    st.metric(
        label="Mulheres Baleadas 18–45a (FC 2025)",
        value=f"{kpis['total_mulheres_fc']}",
        delta=f"{kpis['mulheres_cis_fc']} Mulheres cis | {kpis['mulheres_trans_fc']} Trans/Travestis",
    )

with col_k5:
    st.metric(
        label="Letalidade Armada Feminina (FC)",
        value=f"{kpis['taxa_letalidade_fc']}%",
        delta=f"{kpis['mortas_fc']} Mortas vs. {kpis['feridas_fc']} Feridas",
    )

with col_k6:
    st.metric(
        label=f"Mulheres Negras (ODS 18) & Idade ({stat_mode})",
        value=f"{kpis['pct_negras_identificadas']}% Negras",
        delta=f"{kpis['mulheres_negras_fc']} negras | Idade ({stat_mode}): {kpis['idade_central']} anos",
    )

st.divider()

# ==============================================================================
# ABAS TEMÁTICAS COM RECURSOS DE DRILL-DOWN (FASE 4)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧬 1. Interseccionalidade Gênero × Raça (Mulheres 18–45a • FC 2025)",
    "🚺 2. Feminicídio & Violência nas 27 Capitais (SINESP 2025)",
    "🎯 3. Letalidade Armada, Idade (Média vs. Mediana) & Capitais FC",
    "🔍 4. Drill-Down por Capital, Bairro & Circunstância",
    "🛡️ 5. Funil de Critérios da Equipe, LGPD & 5 V's",
    "🗄️ 6. Banco de Dados & Consulta SQL ao Vivo (Entregável 3)",
])

# ------------------------------------------------------------------------------
# ABA 1: MATRIZ INTERSECCIONAL GÊNERO X RAÇA/COR (MULHERES 18-45 ANOS, CAPITAIS 2025)
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("🧬 Cruzamento Interseccional: Mulher Cis & Mulher Trans/Travesti (18–45 anos) × Raça/Cor (Capitais 2025)")
    st.markdown(
        "Análise das **mulheres entre 18 e 45 anos** vítimas de violência armada nas capitais monitoradas pelo "
        "**Instituto Fogo Cruzado em 2025 (Salvador, Recife, Rio de Janeiro e Belém)**, cruzando **Identidade de Gênero (ODS 5)** "
        "e **Raça/Cor (ODS 18)**."
    )

    matrix_df = build_intersectional_matrix(df_fc, normalize_pct=(scale_mode == "Proporção Relativa (%)"))

    if len(matrix_df) > 0:
        c1, c2 = st.columns([1.15, 1])

        with c1:
            metric_col = "participacao_total_pct" if scale_mode == "Proporção Relativa (%)" else "total_vitimas"
            metric_title = "Participação (%)" if scale_mode == "Proporção Relativa (%)" else "Total de Mulheres Vítimas"

            fig_inter = px.bar(
                matrix_df,
                x="raca",
                y=metric_col,
                color="genero",
                barmode="group",
                text_auto=True,
                title=f"Mulheres (18–45 anos) Baleadas nas Capitais em 2025 por Raça/Cor e Gênero ({metric_title})",
                labels={
                    "raca": "Raça/Cor (ODS 18)",
                    metric_col: metric_title,
                    "genero": "Identidade de Gênero (ODS 5)",
                },
                color_discrete_map={"Mulher cis": "#ff3a21", "Mulher trans e travesti": "#7c3aed"},
            )
            fig_inter.update_layout(height=420)
            st.plotly_chart(fig_inter, use_container_width=True)

        with c2:
            pivot_let = matrix_df.pivot(index="genero", columns="raca", values="taxa_letalidade_pct").fillna(0)
            fig_heat = px.imshow(
                pivot_let,
                text_auto=".1f",
                aspect="auto",
                color_continuous_scale="Reds",
                title="Mapa de Calor: Taxa de Letalidade (% Mortas) por Gênero × Raça/Cor",
                labels={"x": "Raça/Cor (ODS 18)", "y": "Identidade de Gênero (ODS 5)", "color": "Letalidade (%)"},
            )
            fig_heat.update_layout(height=420)
            st.plotly_chart(fig_heat, use_container_width=True)

        c3, c4 = st.columns([1, 1])
        with c3:
            idade_col = "idade_media" if stat_mode == "Média" else "idade_mediana"
            fig_age = px.bar(
                matrix_df,
                x=idade_col,
                y="raca",
                color="genero",
                orientation="h",
                barmode="group",
                text_auto=".1f",
                title=f"{stat_mode} de Idade (Faixa 18–45 Anos) por Raça/Cor e Identidade de Gênero",
                labels={idade_col: f"{stat_mode} de Idade (Anos)", "raca": "Raça/Cor", "genero": "Gênero"},
                color_discrete_map={"Mulher cis": "#ff3a21", "Mulher trans e travesti": "#7c3aed"},
            )
            fig_age.update_layout(height=380)
            st.plotly_chart(fig_age, use_container_width=True)

        with c4:
            st.markdown(f"**📋 Tabela Interseccional ODS 5 × ODS 18 (Alternador: `{stat_mode}`)**")
            st.dataframe(
                matrix_df[[
                    "genero", "raca", "total_vitimas", "total_mortos", "total_feridos",
                    "taxa_letalidade_pct", "pct_acao_policial", "idade_media", "idade_mediana",
                ]].rename(columns={
                    "genero": "Gênero (ODS 5)",
                    "raca": "Raça/Cor (ODS 18)",
                    "total_vitimas": "Vítimas (18-45a)",
                    "total_mortos": "Mortas",
                    "total_feridos": "Feridas",
                    "taxa_letalidade_pct": "Letalidade (%)",
                    "pct_acao_policial": "Ação Policial (%)",
                    "idade_media": "Idade Média",
                    "idade_mediana": "Idade Mediana",
                }),
                use_container_width=True,
                height=340,
            )

# ------------------------------------------------------------------------------
# ABA 2: FEMINICÍDIO & VIOLÊNCIA CONTRA A MULHER NAS 27 CAPITAIS (SINESP 2025)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🚺 Violência contra a Mulher nas 27 Capitais do Brasil em 2025 (Fonte Original SINESP)")
    st.markdown(
        "Recorte estrito da **Fonte Original (`fonte original.xlsx`)** para **Janeiro a Dezembro de 2025**, "
        "contemplando **somente as Capitais do Brasil** e **somente vítimas do sexo feminino** nos eventos de "
        "**Feminicídio**, **Tentativa de feminicídio** e **Estupro**."
    )

    if len(df_sinesp) > 0:
        cap_summary = compute_dynamic_aggregation_by_capital(df_sinesp, stat_mode=stat_mode)

        cs1, cs2 = st.columns([1.15, 1])
        with cs1:
            fig_cap = px.bar(
                cap_summary.head(15),
                x="municipio",
                y=["Feminicídio", "Tentativa de feminicídio"]
                + (["Estupro"] if cap_summary["Estupro"].sum() > 0 else []),
                barmode="stack",
                text_auto=True,
                title="Top 15 Capitais Brasileiras em Vítimas do Sexo Feminino (SINESP 2025)",
                labels={"value": "Vítimas do Sexo Feminino", "municipio": "Capital", "variable": "Evento Criminal"},
                color_discrete_map={
                    "Feminicídio": "#dc2626",
                    "Tentativa de feminicídio": "#fb923c",
                    "Estupro": "#9333ea",
                },
            )
            fig_cap.update_layout(height=430, xaxis_tickangle=-35)
            st.plotly_chart(fig_cap, use_container_width=True)

        with cs2:
            by_month_ev = (
                df_sinesp.groupby(["mes", "nome_mes", "evento"], as_index=False)
                .agg(vitimas_fem=("feminino", "sum"))
                .sort_values("mes")
            )
            fig_m_sin = px.line(
                by_month_ev,
                x="nome_mes",
                y="vitimas_fem",
                color="evento",
                markers=True,
                title="Evolução Mensal nas Capitais (Janeiro a Dezembro de 2025)",
                labels={"vitimas_fem": "Vítimas do Sexo Feminino", "nome_mes": "Mês (2025)", "evento": "Evento"},
                color_discrete_map={
                    "Feminicídio": "#dc2626",
                    "Tentativa de feminicídio": "#fb923c",
                    "Estupro": "#9333ea",
                },
            )
            fig_m_sin.update_layout(height=430)
            st.plotly_chart(fig_m_sin, use_container_width=True)

        # Gráfico Dinâmico Média vs Mediana Mensal por Capital
        fig_central = px.bar(
            cap_summary,
            x="municipio",
            y="metrica_central_mensal",
            color="regiao",
            text_auto=".1f",
            title=f"{stat_mode} Mensal de Vítimas Femininas por Capital em 2025 (Alternador Dinâmico: {stat_mode})",
            labels={
                "municipio": "Capital do Brasil",
                "metrica_central_mensal": f"{stat_mode} de Vítimas Femininas / Mês",
                "regiao": "Macrorregião",
            },
        )
        fig_central.update_layout(height=390, xaxis_tickangle=-35)
        st.plotly_chart(fig_central, use_container_width=True)

# ------------------------------------------------------------------------------
# ABA 3: LETALIDADE ARMADA, IDADE (18-45 ANOS) & CAPITAIS FOGO CRUZADO (2025)
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🎯 Violência Armada contra Mulheres (18–45 anos) nas Capitais em 2025 (Fogo Cruzado)")
    st.markdown(
        "Detalhamento das **77 mulheres entre 18 e 45 anos** (`Mulher cis` e `Mulher trans e travesti`) "
        "baleadas entre **janeiro e dezembro de 2025** nas capitais **Salvador (28)**, **Recife (27)**, "
        "**Rio de Janeiro (20)** e **Belém (2)**."
    )

    if len(df_fc) > 0:
        cfc1, cfc2 = st.columns([1.05, 1])

        with cfc1:
            by_cap_sit = (
                df_fc.groupby(["cidade", "situacao"], as_index=False)
                .agg(vitimas=("is_fatal", "count"))
            )
            fig_cap_fc = px.bar(
                by_cap_sit,
                x="cidade",
                y="vitimas",
                color="situacao",
                barmode="group",
                text_auto=True,
                title="Mulheres (18–45 anos) Mortas vs. Feridas por Capital em 2025",
                labels={"cidade": "Capital", "vitimas": "Número de Mulheres", "situacao": "Situação da Vítima"},
                color_discrete_map={"Morto": "#dc2626", "Ferido": "#f59e0b"},
            )
            fig_cap_fc.update_layout(height=410)
            st.plotly_chart(fig_cap_fc, use_container_width=True)

        with cfc2:
            fig_box = px.box(
                df_fc,
                x="raca",
                y="idade",
                color="situacao",
                points="all",
                title=f"Distribuição Etária (18–45 anos) por Raça/Cor e Situação | {stat_mode}: {kpis['idade_central']} anos",
                labels={"raca": "Raça/Cor (ODS 18)", "idade": "Idade da Vítima (18 a 45 anos)", "situacao": "Situação"},
                color_discrete_map={"Morto": "#dc2626", "Ferido": "#f59e0b"},
            )
            fig_box.update_layout(height=410)
            st.plotly_chart(fig_box, use_container_width=True)

        cfc3, cfc4 = st.columns([1, 1])
        with cfc3:
            by_mot = (
                df_fc.groupby("motivo_principal", as_index=False)
                .agg(Mulheres=("is_fatal", "count"), Mortas=("is_fatal", "sum"))
                .sort_values("Mulheres", ascending=True)
            )
            fig_mot = px.bar(
                by_mot,
                x="Mulheres",
                y="motivo_principal",
                orientation="h",
                color="Mortas",
                text_auto=True,
                color_continuous_scale="Reds",
                title="Motivo Principal das Ocorrências com Mulheres (18–45a) nas Capitais (2025)",
                labels={"motivo_principal": "Motivo Principal"},
            )
            fig_mot.update_layout(height=390)
            st.plotly_chart(fig_mot, use_container_width=True)

        with cfc4:
            by_m_fc = (
                df_fc.groupby(["mes", "nome_mes", "raca"], as_index=False)
                .agg(vitimas=("is_fatal", "count"))
                .sort_values("mes")
            )
            fig_m_fc = px.bar(
                by_m_fc,
                x="nome_mes",
                y="vitimas",
                color="raca",
                text_auto=True,
                title="Sazonalidade Mensal (Jan–Dez 2025) de Mulheres Baleadas por Raça/Cor",
                labels={"nome_mes": "Mês (2025)", "vitimas": "Mulheres Baleadas (18-45a)", "raca": "Raça/Cor"},
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig_m_fc.update_layout(height=390)
            st.plotly_chart(fig_m_fc, use_container_width=True)

# ------------------------------------------------------------------------------
# ABA 4: DRILL-DOWN MULTINÍVEL POR CAPITAL, BAIRRO & CIRCUNSTÂNCIA
# ------------------------------------------------------------------------------
with tab4:
    st.subheader(f"🔍 Drill-Down Interativo nas Capitais (Alternador Ativo: `{stat_mode}`)")
    st.markdown(
        "Navegue hierarquicamente pela **Capital → Bairro → Identidade de Gênero → Raça/Cor → Situação**, "
        "ou compare o ranking completo das **27 Capitais do Brasil** na base SINESP."
    )

    d_col1, d_col2 = st.columns([1.05, 1])
    with d_col1:
        if len(df_fc) > 0:
            cap_fc_sel = st.selectbox(
                "Selecionar Capital para Drill-Down de Bairros (Fogo Cruzado 2025):",
                options=["Todas as Capitais (Salvador, Recife, Rio de Janeiro, Belém)"]
                + sorted(df_fc["cidade"].unique().tolist()),
            )
            df_fc_drill = df_fc if cap_fc_sel.startswith("Todas") else df_fc[df_fc["cidade"] == cap_fc_sel]

            fig_sun = px.sunburst(
                df_fc_drill.groupby(["cidade", "genero", "raca", "situacao"], as_index=False).agg(vitimas=("is_fatal", "count")),
                path=["cidade", "genero", "raca", "situacao"],
                values="vitimas",
                color="raca",
                title="Drill-Down Sunburst: Capital → Gênero → Raça/Cor → Situação (2025)",
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig_sun.update_layout(height=430)
            st.plotly_chart(fig_sun, use_container_width=True)

    with d_col2:
        if len(df_fc) > 0:
            bairros_fc = (
                df_fc_drill.groupby(["cidade", "bairro", "raca", "genero"], as_index=False)
                .agg(
                    Vitimas=("is_fatal", "count"),
                    Mortas=("is_fatal", "sum"),
                    Idade_Media=("idade", "mean"),
                    Idade_Mediana=("idade", "median"),
                )
                .sort_values(["Vitimas", "Mortas"], ascending=False)
            )
            bairros_fc["Idade_Media"] = bairros_fc["Idade_Media"].round(1)
            bairros_fc["Idade_Mediana"] = bairros_fc["Idade_Mediana"].round(1)
            st.markdown("**📍 Detalhamento por Bairro, Raça/Cor e Gênero nas Capitais (Fogo Cruzado 2025)**")
            st.dataframe(bairros_fc, use_container_width=True, height=390)

    if len(df_sinesp) > 0:
        st.markdown(f"**🏛️ Tabela Consolidada das 27 Capitais do Brasil (SINESP 2025 • Soma vs. `{stat_mode}` Mensal)**")
        cap_tbl = compute_dynamic_aggregation_by_capital(df_sinesp, stat_mode=stat_mode)
        st.dataframe(
            cap_tbl.rename(columns={
                "regiao": "Região",
                "uf": "UF",
                "estado": "Estado",
                "municipio": "Capital",
                "meses_com_registro": "Meses c/ Ocorrência",
                "soma_vitimas_fem": "Total Vítimas Femininas (2025)",
                "metrica_central_mensal": f"{stat_mode} Mensal (Vítimas/Mês)",
                "taxa_consumacao_fem_pct": "Taxa de Consumação Feminicídio (%)",
            }),
            use_container_width=True,
            height=420,
        )

# ------------------------------------------------------------------------------
# ABA 5: FUNIL DE CRITÉRIOS DA EQUIPE, GOVERNANÇA LGPD & 5 V'S
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("🛡️ Auditoria do Funil de Inclusão/Exclusão, Conformidade LGPD e Limite 1 GB Aiven")

    f1, f2 = st.columns(2)
    with f1:
        funnel_fc = pd.DataFrame({
            "Etapa do Filtro (Instituto Fogo Cruzado)": [
                "1. Base Bruta Total (2016–2026)",
                "2. Inclusão: Jan–Dez de 2025",
                "3. Inclusão: Somente Capitais (c/ município id.)",
                "4. Inclusão: Mulher cis e Mulher trans/travesti",
                "5. Inclusão: Idade informada entre 18 e 45 anos",
            ],
            "Registros": [45025, 5466, 3026, 223, 77],
        })
        fig_fun_fc = px.funnel(
            funnel_fc,
            x="Registros",
            y="Etapa do Filtro (Instituto Fogo Cruzado)",
            title="Funil de Filtragem Estrita — Fogo Cruzado (45.025 → 77 Mulheres)",
            color_discrete_sequence=["#7c3aed"],
        )
        fig_fun_fc.update_layout(height=360)
        st.plotly_chart(fig_fun_fc, use_container_width=True)

    with f2:
        funnel_sin = pd.DataFrame({
            "Etapa do Filtro (Fonte Original SINESP 2025)": [
                "1. Base Bruta Total (Todos os Eventos/Mun 2025)",
                "2. Inclusão: Estupro, Feminicídio e Tent. Feminicídio",
                "3. Exclusão: Sem município id. + Só 27 Capitais",
                "4. Inclusão: Registros Mensais c/ Vítimas Fem. > 0",
                "5. Total de Vítimas do Sexo Feminino nas Capitais",
            ],
            "Quantidade": [832293, 134478, 648, 496, 1233],
        })
        fig_fun_sin = px.funnel(
            funnel_sin,
            x="Quantidade",
            y="Etapa do Filtro (Fonte Original SINESP 2025)",
            title="Funil de Filtragem Estrita — SINESP (832.293 → 496 Registros / 1.233 Vítimas)",
            color_discrete_sequence=["#ff3a21"],
        )
        fig_fun_sin.update_layout(height=360)
        st.plotly_chart(fig_fun_sin, use_container_width=True)

# ------------------------------------------------------------------------------
# ABA 6: EXPLORADOR DO BANCO DE DADOS & CONSULTA SQL AO VIVO (ENTREGÁVEL 3)
# ------------------------------------------------------------------------------
with tab6:
    import sqlite3

    st.subheader("🗄️ Entregável 3: Base Armazenada em Banco de Dados (Star Schema)")
    st.markdown(
        "Acesso direto e interativo ao **Banco de Dados Relacional (`dw_violencia_interseccional`)** modelado em "
        "**Esquema Estrela (*Star Schema*)**. Você pode inspecionar todas as **4 Tabelas de Dimensão**, **2 Tabelas Fato** "
        "e **2 Views Analíticas**, executar consultas SQL ao vivo e baixar o banco `.db` ou o dump `.sql`."
    )

    if not SQLITE_DB_PATH.exists():
        star_tbls = build_star_schema_tables(df_sinesp_full, df_fc_full)
        build_sqlite_warehouse_and_dump(star_tbls)

    db_col1, db_col2, db_col3 = st.columns(3)
    with db_col1:
        if SQLITE_DB_PATH.exists():
            st.download_button(
                label="⬇️ Baixar Banco SQLite3 (dw_violencia_interseccional.db)",
                data=SQLITE_DB_PATH.read_bytes(),
                file_name="dw_violencia_interseccional.db",
                mime="application/octet-stream",
                use_container_width=True,
            )
    with db_col2:
        if SQL_DUMP_PATH.exists():
            st.download_button(
                label="⬇️ Baixar Dump SQL Completo (DDL + INSERTs .sql)",
                data=SQL_DUMP_PATH.read_bytes(),
                file_name="dump_dw_violencia_interseccional.sql",
                mime="application/sql",
                use_container_width=True,
            )
    with db_col3:
        if SCHEMA_SQL_PATH.exists():
            st.download_button(
                label="⬇️ Baixar Script DDL PostgreSQL Aiven (schema.sql)",
                data=SCHEMA_SQL_PATH.read_bytes(),
                file_name="schema.sql",
                mime="application/sql",
                use_container_width=True,
            )

    with sqlite3.connect(SQLITE_DB_PATH) as conn_ui:
        st.markdown("#### 📊 Quantidade de Dados Armazenados por Entidade/Tabela no Banco")
        summary_rows = []
        for tbl_name, tbl_role, pk_col, fk_cols in [
            ("dim_tempo", "Dimensão Calendário (2025)", "id_tempo", "—"),
            ("dim_localidade", "Dimensão Geográfica (27 Capitais e Bairros)", "id_localidade", "—"),
            ("dim_perfil_vitima", "Dimensão Perfil Interseccional (ODS 5 & ODS 18)", "id_perfil", "—"),
            ("dim_contexto_crime", "Dimensão Contexto e Tipificação Criminal", "id_contexto", "—"),
            ("fato_violencia_sinesp", "Tabela Fato 1: SINESP Capitais 2025 (1.233 vítimas fem.)", "id_fato_sinesp", "id_tempo, id_localidade, id_contexto"),
            ("fato_vitimas_fogo_cruzado", "Tabela Fato 2: Fogo Cruzado Mulheres 18–45a (77 vítimas)", "id_fato_fc", "id_tempo, id_localidade, id_perfil, id_contexto"),
            ("vw_resumo_violencia_sinesp", "View Analítica Desnormalizada SINESP", "— (View)", "JOIN Fato 1 + 3 Dimensões"),
            ("vw_resumo_interseccional_fogo_cruzado", "View Analítica Desnormalizada Fogo Cruzado", "— (View)", "JOIN Fato 2 + 4 Dimensões"),
        ]:
            cnt = conn_ui.execute(f"SELECT COUNT(*) FROM {tbl_name}").fetchone()[0]
            cols_info = conn_ui.execute(f"PRAGMA table_info({tbl_name})").fetchall()
            summary_rows.append({
                "Tabela / View": tbl_name,
                "Papel no Star Schema": tbl_role,
                "Chave Primária (PK)": pk_col,
                "Chaves Estrangeiras (FK)": fk_cols,
                "Qtd. Colunas": len(cols_info),
                "Registros Armazenados": cnt,
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

        st.markdown("#### 💻 Console de Consulta SQL ao Vivo")
        preset_queries = {
            "1. Matriz Interseccional Gênero × Raça/Cor e Letalidade (View Fogo Cruzado)": (
                "SELECT genero, raca_cor, COUNT(*) AS total_vitimas, SUM(is_fatal) AS mortas, "
                "ROUND(AVG(is_fatal)*100, 1) AS letalidade_pct, ROUND(AVG(idade_vitima), 1) AS idade_media "
                "FROM vw_resumo_interseccional_fogo_cruzado "
                "GROUP BY genero, raca_cor ORDER BY total_vitimas DESC;"
            ),
            "2. Ranking das Capitais em Feminicídio e Tentativa de Feminicídio (View SINESP)": (
                "SELECT regiao, uf, municipio AS capital, "
                "SUM(CASE WHEN tipo_evento = 'Feminicídio' THEN vitimas_feminino ELSE 0 END) AS feminicidios, "
                "SUM(CASE WHEN tipo_evento = 'Tentativa de feminicídio' THEN vitimas_feminino ELSE 0 END) AS tentativas, "
                "SUM(vitimas_feminino) AS total_vitimas_femininas "
                "FROM vw_resumo_violencia_sinesp "
                "GROUP BY regiao, uf, municipio ORDER BY total_vitimas_femininas DESC;"
            ),
            "3. Inspecionar Dimensão Perfil da Vítima (dim_perfil_vitima)": "SELECT * FROM dim_perfil_vitima;",
            "4. Inspecionar Dimensão Contexto do Crime (dim_contexto_crime)": "SELECT * FROM dim_contexto_crime;",
            "5. Inspecionar Dimensão Localidade (dim_localidade)": "SELECT * FROM dim_localidade;",
            "6. Inspecionar Dimensão Tempo (dim_tempo)": "SELECT * FROM dim_tempo;",
            "7. Inspecionar Tabela Fato 1 (fato_violencia_sinesp)": "SELECT * FROM fato_violencia_sinesp LIMIT 100;",
            "8. Inspecionar Tabela Fato 2 Anonimizada LGPD (fato_vitimas_fogo_cruzado)": "SELECT * FROM fato_vitimas_fogo_cruzado;",
        }
        chosen_preset = st.selectbox("Escolha uma consulta pronta ou edite o SQL abaixo:", list(preset_queries.keys()))
        custom_sql = st.text_area("Query SQL:", value=preset_queries[chosen_preset], height=100)
        if st.button("▶️ Executar Consulta SQL no Banco", type="primary"):
            try:
                df_sql_out = pd.read_sql_query(custom_sql, conn_ui)
                st.success(f"Consulta executada com sucesso! ({len(df_sql_out)} registros retornados)")
                st.dataframe(df_sql_out, use_container_width=True)
            except Exception as sql_err:
                st.error(f"Erro ao executar SQL: {sql_err}")


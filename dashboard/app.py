"""
FASE 4 & FASE 5: Dashboard Executivo e Interativo de Business Intelligence (Streamlit)
Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)
Alinhado à ODS 5 (Igualdade de Gênero) e à ODS 18 (Igualdade Étnico-Racial).

Destaques para Apresentação em Sala de Aula:
  • 12 Filtros Cruzados Multidimensionais (Período, Trimestre, Mês, Macrorregião, Capital,
    Tipo de Evento SINESP, Identidade de Gênero, Raça/Cor, Faixa Etária, Situação da Vítima,
    Motivo Principal e Envolvimento de Ação Policial) + Botão de Reset Instantâneo
  • Alternadores Dinâmicos de Tendência Central (Média vs. Mediana) e Escala (Absoluto vs. %)
  • 6 Cards de KPIs Executivos + Resumo Inteligente de Insights Automáticos do Recorte
  • 6 Abas Analíticas Completas:
      1. Matriz Interseccional Gênero × Raça/Cor (ODS 5 & ODS 18)
      2. Panorama Nacional das 27 Capitais (SINESP 2025: Feminicídio e Tentativa)
      3. Violência Armada, Perfil Etário (18–45 anos) e Mapa Geográfico Aproximado (LGPD)
      4. Drill-Down Hierárquico Multinível (Sunburst, Treemap, Bairros e Microdados)
      5. Funil de Critérios da Equipe, Governança LGPD e 5 V's do Big Data
      6. Banco de Dados Star Schema & Console SQL ao Vivo (Entregável 3)
"""
import sqlite3
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
from etl.transform import (
    clean_and_optimize_sinesp,
    clean_and_anonymize_fogo_cruzado,
    build_star_schema_tables,
)
from etl.load import build_sqlite_warehouse_and_dump
from dashboard.business_rules import (
    compute_kpi_metrics,
    build_intersectional_matrix,
    compute_dynamic_aggregation_by_capital,
)

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT E ESTILIZAÇÃO EXECUTIVA
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
    .block-container { padding-top: 1.1rem; padding-bottom: 2rem; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.22);
    }
    .ods-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }
    .ods5 { background-color: #e11d48; color: white; }
    .ods18 { background-color: #7c3aed; color: white; }
    .lgpd { background-color: #059669; color: white; }
    .criteria { background-color: #2563eb; color: white; }
    .insight-box {
        background-color: rgba(30, 41, 59, 0.75);
        border-left: 5px solid #e11d48;
        border-radius: 8px;
        padding: 12px 18px;
        margin-top: 8px;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# CARREGAMENTO DE DADOS COM CACHE DE ALTA PERFORMANCE
# ==============================================================================
@st.cache_data(ttl=3600, show_spinner="Carregando Data Warehouse (Capitais 2025 • ODS 5 & ODS 18)...")
def load_team_cohort_datasets(strict_exclude_unidentified_mun: bool = True):
    """
    Carrega as bases tratadas aplicando os Critérios de Inclusão e Exclusão da Equipe.
    Quando strict_exclude_unidentified_mun=False e a planilha bruta estiver disponível,
    inclui também os registros estaduais de Estupro alocados à respectiva Capital/UF.
    """
    use_cached = strict_exclude_unidentified_mun or (not RAW_SINESP_PATH.exists())
    sinesp_raw = extract_sinesp_dataset(RAW_SINESP_PATH, use_cached_csv=use_cached)
    fc_raw = extract_fogo_cruzado_dataset(RAW_FOGO_CRUZADO_PATH, use_cached_csv=True)

    df_sinesp = clean_and_optimize_sinesp(
        sinesp_raw,
        strict_exclude_unidentified_municipality=strict_exclude_unidentified_mun,
    )
    df_fc = clean_and_anonymize_fogo_cruzado(fc_raw)
    return df_sinesp, df_fc


# ==============================================================================
# BARRA LATERAL: PAINEL COMPLETO DE FILTROS PARA APRESENTAÇÃO EM SALA
# ==============================================================================
st.sidebar.markdown("## 🎛️ Central de Filtros & Controles")
st.sidebar.caption("Use os controles abaixo durante a apresentação para cruzar dimensões ao vivo.")

if st.sidebar.button("🔄 Resetar Todos os Filtros (Visão Completa)", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 1. Alternadores Dinâmicos
with st.sidebar.expander("⚡ 1. Alternadores Estatísticos & Escala", expanded=True):
    stat_mode = st.radio(
        "Medida de Tendência Central:",
        options=["Média", "Mediana"],
        index=0,
        horizontal=True,
        key="flt_stat_mode",
        help="Alterna todos os KPIs e gráficos entre Média e Mediana (evitando distorção por outliers).",
    )
    scale_mode = st.radio(
        "Escala dos Gráficos:",
        options=["Valores Absolutos", "Proporção Relativa (%)"],
        index=0,
        horizontal=True,
        key="flt_scale_mode",
        help="Alterna entre número absoluto de vítimas e participação percentual (%).",
    )
    strict_mun_toggle = st.checkbox(
        "Exclusão Estrita: Sem Município Identificado",
        value=True,
        key="flt_strict_mun",
        help=(
            "Na planilha original do SINESP, Feminicídio (292) e Tentativa de feminicídio (941) possuem a Capital identificada. "
            "Já Estupro (18.218) possui a coluna município vazia. Desmarque para incluir Estupro por UF/Capital."
        ),
    )

df_sinesp_full, df_fc_full = load_team_cohort_datasets(
    strict_exclude_unidentified_mun=strict_mun_toggle
)

# 2. Filtros Temporais (Trimestre e Mês de 2025)
with st.sidebar.expander("📅 2. Filtros Temporais (Ano 2025)", expanded=True):
    trimestres_map = {
        1: "1º Trimestre (Jan–Mar)",
        2: "2º Trimestre (Abr–Jun)",
        3: "3º Trimestre (Jul–Set)",
        4: "4º Trimestre (Out–Dez)",
    }
    trimestres_sel_labels = st.multiselect(
        "Trimestres de 2025:",
        options=list(trimestres_map.values()),
        default=list(trimestres_map.values()),
        key="flt_trimestres",
    )
    trimestres_sel = [
        k for k, v in trimestres_map.items() if v in trimestres_sel_labels
    ] or [1, 2, 3, 4]

    meses_do_trimestre = sorted([
        m for m in range(1, 13) if ((m - 1) // 3 + 1) in trimestres_sel
    ])
    meses_nomes_map = {m: f"{m:02d} - {MESES_PT.get(m, str(m))}" for m in meses_do_trimestre}
    meses_sel_labels = st.multiselect(
        "Meses de 2025 (Jan–Dez):",
        options=[meses_nomes_map[m] for m in meses_do_trimestre],
        default=[meses_nomes_map[m] for m in meses_do_trimestre],
        key="flt_meses",
    )
    meses_sel = (
        [int(lbl.split(" - ")[0]) for lbl in meses_sel_labels]
        if meses_sel_labels
        else meses_do_trimestre
    )

# 3. Filtros Geográficos (Macrorregião e Capitais)
with st.sidebar.expander("🌍 3. Filtros Geográficos (Capitais do Brasil)", expanded=True):
    regioes_disp = sorted(
        list(set(df_sinesp_full["regiao"].unique().tolist()) | set(df_fc_full["regiao"].unique().tolist()))
    )
    regioes_sel = st.multiselect(
        "Macrorregião do IBGE:",
        options=regioes_disp,
        default=regioes_disp,
        key="flt_regioes",
    )
    if not regioes_sel:
        regioes_sel = regioes_disp

    only_fc_capitals = st.checkbox(
        "Focar apenas nas 4 Capitais com Microdados Fogo Cruzado (Salvador, Recife, Rio de Janeiro, Belém)",
        value=False,
        key="flt_only_fc_caps",
    )

    capitais_regiao = sorted(
        df_sinesp_full[df_sinesp_full["regiao"].isin(regioes_sel)]["municipio"].unique().tolist()
    )
    if only_fc_capitals:
        fc_caps_set = set(df_fc_full["cidade"].unique().tolist())
        capitais_default = [c for c in capitais_regiao if c in fc_caps_set] or capitais_regiao
    else:
        capitais_default = capitais_regiao

    capitais_sel = st.multiselect(
        "Capitais Selecionadas:",
        options=capitais_regiao,
        default=capitais_default,
        key="flt_capitais",
    )
    if not capitais_sel:
        capitais_sel = capitais_default

# 4. Filtro de Eventos da Fonte Original (SINESP)
with st.sidebar.expander("🏛️ 4. Filtros SINESP (Violência Oficial)", expanded=True):
    eventos_sinesp_disp = sorted(df_sinesp_full["evento"].unique().tolist())
    eventos_sinesp_sel = st.multiselect(
        "Natureza do Evento (SINESP):",
        options=eventos_sinesp_disp,
        default=eventos_sinesp_disp,
        key="flt_eventos_sinesp",
    )
    if not eventos_sinesp_sel:
        eventos_sinesp_sel = eventos_sinesp_disp

# 5. Filtros Interseccionais e Demográficos (ODS 5 & ODS 18 - Fogo Cruzado)
with st.sidebar.expander("🧬 5. Filtros Interseccionais (ODS 5 & ODS 18)", expanded=True):
    generos_fc_disp = sorted(df_fc_full["genero"].unique().tolist())
    generos_sel = st.multiselect(
        "Identidade de Gênero (ODS 5):",
        options=generos_fc_disp,
        default=generos_fc_disp,
        key="flt_generos",
    )
    if not generos_sel:
        generos_sel = generos_fc_disp

    racas_fc_disp = sorted(df_fc_full["raca"].unique().tolist())
    racas_sel = st.multiselect(
        "Raça / Cor (ODS 18):",
        options=racas_fc_disp,
        default=racas_fc_disp,
        key="flt_racas",
    )
    if not racas_sel:
        racas_sel = racas_fc_disp

    idade_range = st.slider(
        "Faixa Etária da Vítima (18 a 45 anos):",
        min_value=18,
        max_value=45,
        value=(18, 45),
        key="flt_idade_range",
    )

    situacoes_disp = sorted(df_fc_full["situacao"].unique().tolist())
    situacoes_sel = st.multiselect(
        "Situação da Vítima (Desfecho):",
        options=situacoes_disp,
        default=situacoes_disp,
        key="flt_situacao",
    )
    if not situacoes_sel:
        situacoes_sel = situacoes_disp

# 6. Filtros de Contexto Operacional (Ação Policial e Motivo Principal)
with st.sidebar.expander("🚨 6. Filtros de Contexto & Ação Policial", expanded=False):
    acao_policial_opt = st.radio(
        "Envolvimento de Ação/Operação Policial:",
        options=["Todos os Registros", "Com Ação Policial", "Sem Ação Policial"],
        index=0,
        key="flt_acao_pol",
    )

    motivos_disp = sorted(df_fc_full["motivo_principal"].unique().tolist())
    motivos_sel = st.multiselect(
        "Motivo Principal do Tiroteio/Ocorrência:",
        options=motivos_disp,
        default=motivos_disp,
        key="flt_motivos",
    )
    if not motivos_sel:
        motivos_sel = motivos_disp

# ==============================================================================
# APLICAÇÃO DOS FILTROS CRUZADOS SOBRE AS DUAS BASES
# ==============================================================================
df_sinesp = df_sinesp_full[
    (df_sinesp_full["mes"].isin(meses_sel))
    & (df_sinesp_full["regiao"].isin(regioes_sel))
    & (df_sinesp_full["municipio"].isin(capitais_sel))
    & (df_sinesp_full["evento"].isin(eventos_sinesp_sel))
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
    & (df_fc_full["situacao"].isin(situacoes_sel))
    & (df_fc_full["motivo_principal"].isin(motivos_sel))
].copy()

if acao_policial_opt == "Com Ação Policial":
    df_fc = df_fc[df_fc["acao_policial"] == 1].copy()
elif acao_policial_opt == "Sem Ação Policial":
    df_fc = df_fc[df_fc["acao_policial"] == 0].copy()

# ==============================================================================
# CABEÇALHO EXECUTIVO E PAINEL DE FILTROS ATIVOS
# ==============================================================================
st.markdown(
    """
    <div>
        <span class="ods-badge ods5">ODS 5 • Igualdade de Gênero</span>
        <span class="ods-badge ods18">ODS 18 • Igualdade Étnico-Racial</span>
        <span class="ods-badge criteria">Coorte 2025 • Capitais do Brasil • Mulheres (18–45 anos)</span>
        <span class="ods-badge lgpd">Governança LGPD • SHA-256 & k-Anonimato</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.title("📊 Observatório Interseccional da Violência contra a Mulher nas Capitais (2025)")

# Barra de Status do Recorte Ativo + Botão de Exportação CSV
kpis = compute_kpi_metrics(df_sinesp, df_fc, stat_mode=stat_mode)

st.markdown(
    f"""
    <div class="insight-box">
        <b>🎯 Síntese Executiva do Recorte Filtrado ({stat_mode}):</b>
        Estão selecionados <b>{len(meses_sel)}/12 meses de 2025</b> em <b>{kpis['capitais_ativas_sinesp']} Capitais</b>
        (<b>{', '.join(regioes_sel)}</b>). Na base oficial <b>SINESP</b>, o recorte soma
        <b>{kpis['total_fem_sinesp']:,} vítimas do sexo feminino</b> (<b>{kpis['vit_feminicidio']} Feminicídios consumados</b> e
        <b>{kpis['vit_tentativa']} Tentativas de feminicídio</b> — taxa de consumação de <b>{kpis['taxa_letalidade_feminicidio_pct']}%</b>).
        Nos microdados do <b>Instituto Fogo Cruzado</b> (faixa <b>{idade_range[0]}–{idade_range[1]} anos</b>), há
        <b>{kpis['total_mulheres_fc']} mulheres baleadas</b> (<b>{kpis['mulheres_cis_fc']} Mulheres cis</b> e
        <b>{kpis['mulheres_trans_fc']} Mulheres trans/travestis</b>), com <b>{kpis['taxa_letalidade_fc']}% de letalidade</b>
        (<b>{kpis['mortas_fc']} mortas</b> e <b>{kpis['feridas_fc']} feridas</b>), onde <b>{kpis['pct_negras_identificadas']}% são Mulheres Negras</b>
        (dentre as vítimas com raça identificada) e a <b>{stat_mode} de idade é de {kpis['idade_central']} anos</b>.
    </div>
    """.replace(",", "."),
    unsafe_allow_html=True,
)

# ==============================================================================
# SEÇÃO SUPERIOR: 6 CARDS DE KPIS EXECUTIVOS (FASE 4)
# ==============================================================================
col_k1, col_k2, col_k3, col_k4, col_k5, col_k6 = st.columns(6)

with col_k1:
    st.metric(
        label="Vítimas Femininas (SINESP)",
        value=f"{kpis['total_fem_sinesp']:,}".replace(",", "."),
        delta=f"{kpis['vit_por_capital']} vítimas/capital ({stat_mode})",
    )

with col_k2:
    st.metric(
        label="Feminicídios Consumados",
        value=f"{kpis['vit_feminicidio']:,}".replace(",", "."),
        delta=f"{kpis['taxa_letalidade_feminicidio_pct']}% taxa de consumação",
    )

with col_k3:
    st.metric(
        label="Tentativas de Feminicídio",
        value=f"{kpis['vit_tentativa']:,}".replace(",", "."),
        delta=(
            f"+ {kpis['vit_estupro']:,} Estupros (UF)".replace(",", ".")
            if kpis["vit_estupro"] > 0
            else f"Em {kpis['capitais_ativas_sinesp']} Capitais ativas"
        ),
    )

with col_k4:
    st.metric(
        label=f"Mulheres Baleadas ({idade_range[0]}–{idade_range[1]}a)",
        value=f"{kpis['total_mulheres_fc']}",
        delta=f"{kpis['mulheres_cis_fc']} Cis | {kpis['mulheres_trans_fc']} Trans/Travestis",
    )

with col_k5:
    st.metric(
        label="Letalidade Armada (FC)",
        value=f"{kpis['taxa_letalidade_fc']}%",
        delta=f"{kpis['mortas_fc']} Mortas vs. {kpis['feridas_fc']} Feridas",
    )

with col_k6:
    st.metric(
        label=f"Mulheres Negras & Idade ({stat_mode})",
        value=f"{kpis['pct_negras_identificadas']}% Negras",
        delta=f"{kpis['mulheres_negras_fc']} negras | {stat_mode}: {kpis['idade_central']} anos",
    )

with st.expander("📋 Critérios Metodológicos da Equipe & Download Rápido dos Dados Filtrados", expanded=False):
    c_inc, c_exc, c_dl = st.columns([1.15, 1.15, 0.9])
    with c_inc:
        st.markdown(
            "**✅ Critérios de Inclusão Definidos pela Equipe:**\n"
            "- **Período:** Janeiro a Dezembro de 2025 (`01/2025` a `12/2025`)\n"
            "- **Geografia:** Somente **Capitais do Brasil** (`27` capitais no SINESP; `Salvador`, `Recife`, `Rio de Janeiro` e `Belém` no Fogo Cruzado)\n"
            "- **Eventos (SINESP):** `Estupro`, `Feminicídio` e `Tentativa de feminicídio`\n"
            "- **Sexo (SINESP):** Somente vítimas do **sexo feminino** (`feminino > 0`)\n"
            "- **Faixa Etária (Fogo Cruzado):** Mulheres entre **18 e 45 anos**\n"
            "- **Gênero (Fogo Cruzado):** Somente `Mulher cis` e `Mulher trans e travesti`"
        )
    with c_exc:
        st.markdown(
            "**🚫 Critérios de Exclusão Definidos pela Equipe:**\n"
            "- **Sem Gênero Informado (Fogo Cruzado):** Excluídos `1.240` registros sem gênero e `40.560` registros masculinos\n"
            "- **Sem Município Identificado:** Excluídos registros sem município ou do interior\n"
            "- **Sem Idade Informada (Fogo Cruzado):** Excluídos `96` registros de mulheres nas capitais em 2025 sem idade preenchida e `50` fora da faixa 18–45 anos"
        )
    with c_dl:
        st.markdown("**⬇️ Exportar Recorte Atual (CSV):**")
        st.download_button(
            "📥 Baixar SINESP Filtrado (.csv)",
            data=df_sinesp.to_csv(index=False).encode("utf-8"),
            file_name="sinesp_capitais_2025_filtrado.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "📥 Baixar Fogo Cruzado Filtrado (.csv)",
            data=df_fc.to_csv(index=False).encode("utf-8"),
            file_name="fogo_cruzado_mulheres_18_45_filtrado.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.divider()

# ==============================================================================
# ABAS TEMÁTICAS PARA APRESENTAÇÃO EM SALA
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧬 1. Interseccionalidade Gênero × Raça (ODS 5 & 18)",
    "🚺 2. Ranking das 27 Capitais (SINESP 2025)",
    "🎯 3. Violência Armada, Idade & Mapa Espacial (FC 2025)",
    "🔍 4. Drill-Down por Capital, Bairro & Microdados",
    "🛡️ 5. Funil de Critérios da Equipe, LGPD & 5 V's",
    "🗄️ 6. Banco de Dados Star Schema & SQL ao Vivo",
])

# ------------------------------------------------------------------------------
# ABA 1: MATRIZ INTERSECCIONAL GÊNERO X RAÇA/COR (ODS 5 & ODS 18)
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("🧬 Cruzamento Interseccional: Identidade de Gênero (ODS 5) × Raça/Cor (ODS 18)")
    st.markdown(
        "Análise da vitimização e letalidade armada de **mulheres entre 18 e 45 anos (`Mulher cis` e `Mulher trans e travesti`)** "
        "nas capitais monitoradas pelo **Instituto Fogo Cruzado em 2025 (`Salvador`, `Recife`, `Rio de Janeiro` e `Belém`)**."
    )

    matrix_df = build_intersectional_matrix(df_fc, normalize_pct=(scale_mode == "Proporção Relativa (%)"))

    if len(matrix_df) > 0:
        c1, c2 = st.columns([1.15, 1])

        with c1:
            metric_col = "participacao_total_pct" if scale_mode == "Proporção Relativa (%)" else "total_vitimas"
            metric_title = "Participação Relativa (%)" if scale_mode == "Proporção Relativa (%)" else "Total de Mulheres Baleadas"

            fig_inter = px.bar(
                matrix_df,
                x="raca",
                y=metric_col,
                color="genero",
                barmode="group",
                text_auto=True,
                title=f"Mulheres ({idade_range[0]}–{idade_range[1]} anos) por Raça/Cor e Identidade de Gênero ({metric_title})",
                labels={
                    "raca": "Raça/Cor (ODS 18)",
                    metric_col: metric_title,
                    "genero": "Identidade de Gênero (ODS 5)",
                },
                color_discrete_map={"Mulher cis": "#e11d48", "Mulher trans e travesti": "#7c3aed"},
            )
            fig_inter.update_layout(height=420, legend_title_text="Gênero (ODS 5)")
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

        c3, c4 = st.columns([1, 1.1])
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
                title=f"{stat_mode} de Idade ({idade_range[0]}–{idade_range[1]} Anos) por Raça/Cor e Gênero",
                labels={idade_col: f"{stat_mode} de Idade (Anos)", "raca": "Raça/Cor", "genero": "Gênero"},
                color_discrete_map={"Mulher cis": "#e11d48", "Mulher trans e travesti": "#7c3aed"},
            )
            fig_age.update_layout(height=380)
            st.plotly_chart(fig_age, use_container_width=True)

        with c4:
            st.markdown(f"**📋 Matriz Analítica Interseccional ODS 5 × ODS 18 (Alternador: `{stat_mode}`)**")
            st.dataframe(
                matrix_df[[
                    "genero", "raca", "total_vitimas", "total_mortos", "total_feridos",
                    "taxa_letalidade_pct", "pct_acao_policial", "idade_media", "idade_mediana",
                ]].rename(columns={
                    "genero": "Gênero (ODS 5)",
                    "raca": "Raça/Cor (ODS 18)",
                    "total_vitimas": "Vítimas",
                    "total_mortos": "Mortas",
                    "total_feridos": "Feridas",
                    "taxa_letalidade_pct": "Letalidade (%)",
                    "pct_acao_policial": "Em Ação Policial (%)",
                    "idade_media": "Idade Média",
                    "idade_mediana": "Idade Mediana",
                }),
                use_container_width=True,
                height=340,
            )
    else:
        st.warning("Nenhum registro encontrado no Fogo Cruzado para a combinação atual de filtros.")

# ------------------------------------------------------------------------------
# ABA 2: RANKING DAS 27 CAPITAIS & SAZONALIDADE (SINESP 2025)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🚺 Violência contra a Mulher nas 27 Capitais do Brasil em 2025 (Fonte Oficial SINESP)")
    st.markdown(
        "Comparativo entre as **27 Capitais Estaduais/Distrital** no ano de **2025**, considerando exclusivamente "
        "**vítimas do sexo feminino** nos crimes de **Feminicídio**, **Tentativa de feminicídio** e **Estupro**."
    )

    if len(df_sinesp) > 0:
        cap_summary = compute_dynamic_aggregation_by_capital(df_sinesp, stat_mode=stat_mode)

        cs1, cs2 = st.columns([1.15, 1])
        with cs1:
            ev_cols_plot = [
                c for c in ["Feminicídio", "Tentativa de feminicídio", "Estupro"]
                if c in cap_summary.columns and cap_summary[c].sum() > 0
            ]
            fig_cap = px.bar(
                cap_summary.head(15),
                x="municipio",
                y=ev_cols_plot,
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
                title="Curva Sazonal Mensal nas Capitais Selecionadas (Jan–Dez 2025)",
                labels={"vitimas_fem": "Vítimas do Sexo Feminino", "nome_mes": "Mês (2025)", "evento": "Evento"},
                color_discrete_map={
                    "Feminicídio": "#dc2626",
                    "Tentativa de feminicídio": "#fb923c",
                    "Estupro": "#9333ea",
                },
            )
            fig_m_sin.update_layout(height=430)
            st.plotly_chart(fig_m_sin, use_container_width=True)

        cs3, cs4 = st.columns([1.15, 1])
        with cs3:
            fig_central = px.bar(
                cap_summary,
                x="municipio",
                y="metrica_central_mensal",
                color="regiao",
                text_auto=".1f",
                title=f"{stat_mode} Mensal de Vítimas Femininas por Capital em 2025 (Alternador: {stat_mode})",
                labels={
                    "municipio": "Capital do Brasil",
                    "metrica_central_mensal": f"{stat_mode} de Vítimas / Mês",
                    "regiao": "Macrorregião",
                },
            )
            fig_central.update_layout(height=400, xaxis_tickangle=-35)
            st.plotly_chart(fig_central, use_container_width=True)

        with cs4:
            by_regiao = (
                df_sinesp.groupby(["regiao", "evento"], as_index=False)
                .agg(vitimas_fem=("feminino", "sum"))
            )
            fig_reg = px.bar(
                by_regiao,
                x="regiao",
                y="vitimas_fem",
                color="evento",
                barmode="group",
                text_auto=True,
                title="Distribuição por Macrorregião do IBGE (Capitais 2025)",
                labels={"regiao": "Macrorregião", "vitimas_fem": "Vítimas Femininas", "evento": "Evento"},
                color_discrete_map={
                    "Feminicídio": "#dc2626",
                    "Tentativa de feminicídio": "#fb923c",
                    "Estupro": "#9333ea",
                },
            )
            fig_reg.update_layout(height=400)
            st.plotly_chart(fig_reg, use_container_width=True)
    else:
        st.warning("Nenhum registro encontrado no SINESP para a combinação atual de filtros.")

# ------------------------------------------------------------------------------
# ABA 3: VIOLÊNCIA ARMADA, IDADE (18-45 ANOS) & MAPA ESPACIAL LGPD (FC 2025)
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🎯 Violência Armada, Perfil Etário (18–45 anos) e Distribuição Espacial (LGPD)")
    st.markdown(
        "Análise detalhada das mulheres baleadas nas capitais monitoradas pelo **Instituto Fogo Cruzado em 2025**, "
        "incluindo distribuição etária (**Média vs. Mediana**), circunstâncias, local da ocorrência e **Mapa Espacial com *k*-Anonimato LGPD**."
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
                title="Mulheres Baleadas Mortas vs. Feridas por Capital Monitorada (2025)",
                labels={"cidade": "Capital", "vitimas": "Número de Mulheres", "situacao": "Situação da Vítima"},
                color_discrete_map={"Morto": "#dc2626", "Ferido": "#f59e0b"},
            )
            fig_cap_fc.update_layout(height=400)
            st.plotly_chart(fig_cap_fc, use_container_width=True)

        with cfc2:
            fig_box = px.box(
                df_fc,
                x="raca",
                y="idade",
                color="situacao",
                points="all",
                hover_data=["cidade", "bairro", "genero", "motivo_principal"],
                title=f"Distribuição Etária ({idade_range[0]}–{idade_range[1]}a) por Raça/Cor | {stat_mode}: {kpis['idade_central']} anos",
                labels={"raca": "Raça/Cor (ODS 18)", "idade": "Idade da Vítima (Anos)", "situacao": "Situação"},
                color_discrete_map={"Morto": "#dc2626", "Ferido": "#f59e0b"},
            )
            fig_box.update_layout(height=400)
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
                title="Motivo Principal das Ocorrências com Mulheres Baleadas (2025)",
                labels={"motivo_principal": "Motivo Principal"},
            )
            fig_mot.update_layout(height=390)
            st.plotly_chart(fig_mot, use_container_width=True)

        with cfc4:
            df_map = df_fc.dropna(subset=["lat_aprox", "lon_aprox"]).copy()
            if len(df_map) > 0:
                fig_map = px.scatter_mapbox(
                    df_map,
                    lat="lat_aprox",
                    lon="lon_aprox",
                    color="situacao",
                    symbol="raca",
                    size_max=14,
                    zoom=3.4,
                    center={"lat": -12.9, "lon": -41.0},
                    mapbox_style="carto-darkmatter",
                    hover_name="cidade",
                    hover_data={
                        "bairro": True,
                        "genero": True,
                        "raca": True,
                        "idade": True,
                        "motivo_principal": True,
                        "lat_aprox": True,
                        "lon_aprox": True,
                    },
                    color_discrete_map={"Morto": "#ef4444", "Ferido": "#f59e0b"},
                    title="Mapa Espacial Anonimizado (LGPD: Coordenadas Truncadas 2 Casas ~1,1 km)",
                )
                fig_map.update_layout(height=390, margin={"r": 0, "t": 40, "l": 0, "b": 0})
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("Sem coordenadas aproximadas disponíveis para o filtro atual.")
    else:
        st.warning("Nenhum registro encontrado no Fogo Cruzado para a combinação atual de filtros.")

# ------------------------------------------------------------------------------
# ABA 4: DRILL-DOWN MULTINÍVEL POR CAPITAL, BAIRRO & EXPLORADOR DE MICRODADOS
# ------------------------------------------------------------------------------
with tab4:
    st.subheader(f"🔍 Drill-Down Interativo por Capital, Bairro e Microdados (Alternador: `{stat_mode}`)")
    st.markdown(
        "Explore a hierarquia completa **Capital → Identidade de Gênero → Raça/Cor → Situação → Bairro** "
        "para responder perguntas específicas durante a apresentação em sala."
    )

    d_col1, d_col2 = st.columns([1.05, 1])
    with d_col1:
        if len(df_fc) > 0:
            cap_fc_sel = st.selectbox(
                "Selecionar Capital para Drill-Down de Bairros (Fogo Cruzado 2025):",
                options=["Todas as Capitais Selecionadas"] + sorted(df_fc["cidade"].unique().tolist()),
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
            st.markdown("**📍 Ranking de Bairros por Raça/Cor e Gênero nas Capitais (Fogo Cruzado 2025)**")
            st.dataframe(bairros_fc, use_container_width=True, height=390)

    if len(df_sinesp) > 0:
        st.markdown(f"**🏛️ Tabela Completa das Capitais do Brasil (SINESP 2025 • Soma Anual vs. `{stat_mode}` Mensal)**")
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
            height=380,
        )

    if len(df_fc) > 0:
        with st.expander("🔎 Inspecionar Microdados Individuais Anonimizados (LGPD - Fogo Cruzado 2025)", expanded=False):
            st.dataframe(
                df_fc[[
                    "data", "cidade", "bairro", "genero", "raca", "idade", "faixa_etaria",
                    "situacao", "motivo_principal", "circunstancias", "local", "acao_policial",
                    "vitima_hash", "lat_aprox", "lon_aprox",
                ]],
                use_container_width=True,
            )

# ------------------------------------------------------------------------------
# ABA 5: FUNIL DE CRITÉRIOS DA EQUIPE, GOVERNANÇA LGPD & 5 V'S
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("🛡️ Auditoria do Funil de Inclusão/Exclusão, Conformidade LGPD e 5 V's do Big Data")

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
            title="Funil Metodológico — Fogo Cruzado (45.025 → 77 Mulheres)",
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
                "4. Consolidação Mensal c/ Vítimas Fem. > 0",
                "5. Total de Vítimas do Sexo Feminino nas Capitais",
            ],
            "Quantidade": [832293, 134478, 648, 399, 1233],
        })
        fig_fun_sin = px.funnel(
            funnel_sin,
            x="Quantidade",
            y="Etapa do Filtro (Fonte Original SINESP 2025)",
            title="Funil Metodológico — SINESP (832.293 → 399 Registros / 1.233 Vítimas)",
            color_discrete_sequence=["#e11d48"],
        )
        fig_fun_sin.update_layout(height=360)
        st.plotly_chart(fig_fun_sin, use_container_width=True)

    st.markdown("#### 📚 Resumo dos 5 V's do Big Data e Governança LGPD para Apresentação")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.info(
            "**📈 Os 5 V's do Big Data no Projeto:**\n"
            "1. **Volume:** `877.318` linhas brutas (`> 360 MB` em XML) otimizadas em `< 1 MB` (`144 KB` no banco `.db`), respeitando o limite de 1 GB da Aiven Cloud.\n"
            "2. **Variedade:** Integração de estatísticas oficiais macro-governamentais (SINESP) com microdados de sociedade civil (Fogo Cruzado) via *Star Schema*.\n"
            "3. **Velocidade:** Índices B-Tree relacionais e cache `@st.cache_data` para resposta sub-segundo nos 12 filtros cruzados.\n"
            "4. **Veracidade:** Saneamento algorítmico de coordenadas GPS fora de escala, conversão de datas seriais e exclusão de registros sem idade/gênero/município.\n"
            "5. **Valor:** Inteligência interseccional acionável alinhada à **ODS 5** e à **ODS 18**."
        )
    with v_col2:
        st.success(
            "**🛡️ Conformidade com a LGPD (Lei nº 13.709/2018):**\n"
            "- **Minimização (Art. 6º, III):** Exclusão de 11 colunas de risco de reidentificação (`endereco`, `ocorrencia_numero`, `cargo_agente`, `corporacao`, `unidade`, etc.).\n"
            "- **Pseudonimização (Arts. 12 e 13):** Hash criptográfico irreversível **SHA-256 com *salt*** (`vitima_hash_lgpd` e `ocorrencia_hash`).\n"
            "- **Generalização Espacial (*k*-Anonimato):** Truncamento de coordenadas geográficas em 2 casas decimais (`lat_aprox`, `lon_aprox` ~ 1,1 km)."
        )

# ------------------------------------------------------------------------------
# ABA 6: EXPLORADOR DO BANCO DE DADOS & CONSULTA SQL AO VIVO (ENTREGÁVEL 3)
# ------------------------------------------------------------------------------
with tab6:
    st.subheader("🗄️ Entregável 3: Base Armazenada em Banco de Dados (Star Schema)")
    st.markdown(
        "Acesso direto e interativo ao **Banco de Dados Relacional (`dw_violencia_interseccional`)** modelado em "
        "**Esquema Estrela (*Star Schema*)**. Inspecione as **4 Tabelas de Dimensão**, **2 Tabelas Fato** "
        "e **2 Views Analíticas**, execute consultas SQL ao vivo durante a apresentação e baixe os artefatos do banco."
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

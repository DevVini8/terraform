"""Visão integrada mensal da violência contra a mulher nas capitais brasileiras."""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from etl.config import MESES_PT
from etl.extract import extract_sinesp_dataset, extract_fogo_cruzado_dataset
from etl.transform import clean_and_optimize_sinesp, clean_and_anonymize_fogo_cruzado
from dashboard.business_rules import build_unified_dataset

st.set_page_config(
    page_title="Violência contra a Mulher nas Capitais (2025)",
    layout="wide",
    initial_sidebar_state="collapsed",
)

dashboard_style = st.empty()
dashboard_css = """
<style>
    .stApp { background: #FFFFFF; color: #28323E; }
    [data-testid="stHeader"] { display: none; }
    .block-container { max-width: 1800px; padding: 1rem 1.25rem 1rem; }
    [data-testid="stVerticalBlock"] { gap: .55rem; }
    h1 { font-size: 1.4rem !important; font-weight: 650 !important;
         padding: .35rem 0 .8rem !important; line-height: 1.4 !important;
         margin: 0 !important; letter-spacing: -.025em; }
    h2, h3 { font-size: .92rem !important; padding: 0 !important; }
    [data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #CDD3DB;
        border-radius: 3px; padding: .55rem .8rem; min-height: 86px; }
    [data-testid="stMetricLabel"] { color: #5C6876; font-size: .73rem; }
    [data-testid="stMetricValue"] { color: #34465B; font-size: 1.8rem; font-weight: 600; }
    [data-testid="stPlotlyChart"] { background: #FFFFFF; border: 1px solid #CDD3DB;
        border-radius: 3px; padding: 0; }
    [data-testid="stWidgetLabel"] p { font-size: .73rem; color: #526171; font-weight: 600; }
    [data-testid="stCaptionContainer"] p { color: #76818D; font-size: .72rem; margin: 0; }
    [data-testid="stDataFrame"] { border: 1px solid #CDD3DB; border-radius: 3px; }
    [data-baseweb="select"] > div { background: #FFFFFF; border-color: #CBD2DA;
        border-radius: 2px; min-height: 34px; font-size: .78rem; }
    [data-testid="stSelectbox"] { margin-bottom: 0; }
    [data-testid="stDownloadButton"] button { background: #F2F4F6; color: #34465B;
        border: 1px solid #CBD2DA; font-size: .78rem; min-height: 32px; }
    [data-testid="stExpander"] { border-radius: 3px; }
    @media (max-width: 768px) { .block-container { padding: 1rem .7rem; } }
</style>
"""

pio.templates["observatorio"] = go.layout.Template(layout=dict(
    paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
    font=dict(family="Segoe UI, Arial, sans-serif", color="#586575", size=11),
    title=dict(font=dict(size=14, color="#34465B"), x=.03, xanchor="left"),
    colorway=["#4B83D1", "#35A58A", "#8B78CE", "#55A9C4", "#CF81A3"],
    margin=dict(l=12, r=16, t=46, b=36), height=260,
    xaxis=dict(showgrid=False, zeroline=False, automargin=True),
    yaxis=dict(gridcolor="#EEF0F3", zeroline=False, automargin=True),
    legend=dict(title_text="", orientation="h", y=-.25, x=0, font=dict(size=10)),
    hoverlabel=dict(bgcolor="#FFFFFF", font_color="#28323E"),
))
px.defaults.template = "observatorio"


@st.cache_data(ttl=3600)
def carregar_dados():
    official = clean_and_optimize_sinesp(extract_sinesp_dataset(use_cached_csv=True))
    individual = clean_and_anonymize_fogo_cruzado(extract_fogo_cruzado_dataset(use_cached_csv=True))
    return build_unified_dataset(official, individual)


base = carregar_dados()
st.title("Violência contra a mulher | Capitais brasileiras · 2025")

base["faixa_idade"] = pd.cut(
    base["idade"], bins=[17, 24, 34, 45],
    labels=["18 a 24 anos", "25 a 34 anos", "35 a 45 anos"],
).astype("string").fillna("Idade não informada")

# Uma opção visível por filtro; "Todos" mantém todas as categorias no recorte.
with st.container(border=True):
    f1, f2, f3, f4, f5, f6, f7, f8 = st.columns([1, 1.25, .9, 1.35, 1.2, 1, 1.2, .85], gap="small")
    regiao = f1.selectbox("Região", ["Todos", *sorted(base["regiao"].unique())], key="regiao")
    geographic = base if regiao == "Todos" else base[base["regiao"] == regiao]
    capital = f2.selectbox("Capital", ["Todos", *sorted(geographic["municipio"].unique())], key="capital")
    mes = f3.selectbox("Mês", ["Todos", *sorted(base["mes"].unique())],
                      format_func=lambda v: "Todos" if v == "Todos" else MESES_PT[v], key="mes")
    tipo = f4.selectbox("Tipo de violência", ["Todos", *sorted(base["tipo_violencia"].unique())], key="tipo_violencia")
    genero = f5.selectbox("Gênero", ["Todos", *sorted(base["genero"].unique())], key="genero")
    raca = f6.selectbox("Raça/Cor", ["Todos", *sorted(base["raca"].unique())], key="raca")
    idade = f7.selectbox("Faixa etária", ["Todos", "18 a 24 anos", "25 a 34 anos", "35 a 45 anos", "Idade não informada"],
                        key="faixa_idade")
    stat_mode = f8.selectbox("Estatística", ["Média", "Mediana"], key="estatistica")

filtered = base.copy()
for column, selection in [
    ("regiao", regiao), ("municipio", capital), ("mes", mes),
    ("tipo_violencia", tipo), ("genero", genero), ("raca", raca), ("faixa_idade", idade),
]:
    if selection != "Todos":
        filtered = filtered[filtered[column] == selection]
meses_sel = [mes] if mes != "Todos" else sorted(base["mes"].unique())

table_height = 143
if filtered.empty:
    st.info("Sem dados para os filtros selecionados.")
else:
    total = int(filtered["quantidade"].sum())
    identified_race = filtered[filtered["raca"] != "Não informado"]
    race_total = identified_race["quantidade"].sum()
    black_total = identified_race.loc[
        identified_race["raca"].isin(["Negra", "Preta", "Parda"]), "quantidade"
    ].sum()
    with_age = filtered[filtered["idade"].notna()]
    age_total = with_age["quantidade"].sum()
    mean_age = (with_age["idade"] * with_age["quantidade"]).sum() / age_total if age_total else None

    main, geography = st.columns([2.15, 1], gap="small")
    with main:
        c1, c2, c3, c4 = st.columns(4, gap="small")
        c1.metric("Registros de vítimas", f"{total:,}".replace(",", "."))
        c2.metric("Capitais", filtered["municipio"].nunique())
        c3.metric("Negras · raça informada", f"{black_total / race_total * 100:.1f}%" if race_total else "N/D",
                  help=f"Raça informada em {int(race_total)} registros do recorte.")
        c4.metric("Idade média informada", f"{mean_age:.1f} anos" if mean_age is not None else "N/D",
                  help=f"Idade informada em {int(age_total)} registros do recorte.")

        st.markdown("**Distribuição por tipo de violência**")
        by_type_month = filtered.groupby(["tipo_violencia", "mes"])["quantidade"].sum().unstack(fill_value=0)
        by_type_month = by_type_month.reindex(columns=meses_sel, fill_value=0)
        summary = pd.DataFrame({
            "Tipo de violência": by_type_month.index,
            "Registros": by_type_month.sum(axis=1).values,
            "% do recorte": (by_type_month.sum(axis=1) / total * 100).round(1).values,
            f"{stat_mode} mensal": (
                by_type_month.mean(axis=1) if stat_mode == "Média" else by_type_month.median(axis=1)
            ).round(1).values,
        })
        table_height = (len(summary) + 1) * 35 + 3
        st.dataframe(summary, width="stretch", height=table_height, row_height=35, hide_index=True,
                     column_config={"% do recorte": st.column_config.NumberColumn(format="%.1f%%")})

        monthly_panel, profile_panel = st.columns([1.1, 1], gap="small")
        with monthly_panel:
            monthly = filtered.groupby("mes")["quantidade"].sum().reindex(meses_sel, fill_value=0).reset_index()
            monthly["Mês"] = monthly["mes"].map(lambda m: MESES_PT[m][:3])
            fig_month = px.bar(
                monthly, x="Mês", y="quantidade", text_auto=True,
                title="Registros por mês", color_discrete_sequence=["#4B83D1"],
                labels={"quantidade": "Registros de vítimas"},
            )
            fig_month.update_traces(textposition="outside", cliponaxis=False)
            fig_month.update_layout(xaxis_title=None, yaxis_title=None)
            fig_month.update_yaxes(range=[0, monthly["quantidade"].max() * 1.25])
            st.plotly_chart(fig_month, width="stretch", height="stretch", key="month-chart", theme=None, config={"displayModeBar": False})
        with profile_panel:
            profile = filtered.groupby("raca", as_index=False)["quantidade"].sum().sort_values("quantidade")
            fig_profile = px.bar(
                profile, y="raca", x="quantidade", orientation="h", text_auto=True,
                title="Registros por raça/cor", color_discrete_sequence=["#35A58A"],
                labels={"quantidade": "Registros de vítimas", "raca": "Raça/Cor"},
            )
            race_colors = {
                "Negra": "#35A58A", "Preta": "#35A58A", "Parda": "#8B78CE",
                "Branca": "#4B83D1", "Amarela": "#55A9C4", "Indígena": "#CF81A3",
                "Não informado": "#A6B3C1",
            }
            fig_profile.update_traces(
                textposition="outside", cliponaxis=False,
                marker_color=profile["raca"].map(race_colors).fillna("#8B78CE").tolist(),
            )
            fig_profile.update_layout(xaxis_title=None, yaxis_title=None)
            fig_profile.update_xaxes(range=[0, profile["quantidade"].max() * 1.3])
            st.plotly_chart(fig_profile, width="stretch", height="stretch", key="profile-chart", theme=None, config={"displayModeBar": False})

    with geography:
        ranking = filtered.groupby(["municipio", "regiao"], as_index=False)["quantidade"].sum().sort_values("quantidade")
        fig_capital = px.bar(
            ranking, y="municipio", x="quantidade", orientation="h", text_auto=True,
            title="Registros por capital", color="regiao",
            color_discrete_map={
                "Norte": "#35A58A", "Nordeste": "#4B83D1", "Centro-Oeste": "#8B78CE",
                "Sudeste": "#55A9C4", "Sul": "#6976C7",
            },
            category_orders={"municipio": ranking["municipio"].iloc[::-1].tolist()},
            labels={"municipio": "Capital", "quantidade": "Registros de vítimas", "regiao": "Região"},
        )
        fig_capital.update_traces(textposition="outside", cliponaxis=False)
        fig_capital.update_layout(height=max(394 + table_height, len(ranking) * 30 + 125),
                                  xaxis_title=None, yaxis_title=None, bargap=.22,
                                  legend=dict(y=-.035, x=0, yanchor="top"),
                                  margin=dict(l=10, r=30, t=46, b=90))
        fig_capital.update_xaxes(range=[0, ranking["quantidade"].max() * 1.25])
        st.plotly_chart(fig_capital, width="stretch", height="stretch", key="capital-chart", theme=None, config={"displayModeBar": False})

with st.expander("Base detalhada e exportação"):
    if not filtered.empty:
        keys = ["ano", "mes", "regiao", "uf", "municipio"]
        detail = filtered.pivot_table(
            index=keys, columns="tipo_violencia", values="quantidade", aggfunc="sum", fill_value=0,
        ).reset_index()
        detail.columns.name = None
        detail = detail.rename(columns={"ano": "Ano", "mes": "Mês", "regiao": "Região", "uf": "UF", "municipio": "Capital"})
        st.dataframe(detail, width="stretch", hide_index=True, height=250)
    st.download_button(
        "Baixar base unificada filtrada (CSV)",
        data=filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="base_unificada_filtrada.csv", mime="text/csv",
    )

with st.expander("Sobre os dados e os indicadores"):
    st.write(
        "Fontes: SINESP/MJSP e Instituto Fogo Cruzado. "
        "Os registros oficiais incluem vítimas do sexo feminino; "
        "os de violência armada incluem mulheres cis e trans/travestis de 18 a 45 anos. "
        "Idade, raça e identidade de gênero ausentes permanecem como não informadas. "
        "Ao selecionar um perfil específico, somente os registros com essa informação são incluídos. "
        "Os tipos de violência não são mutuamente exclusivos, e pode haver sobreposição entre fontes. "
        "A procedência é preservada no CSV para rastreabilidade."
    )

# Reserva a área visível ao painel; detalhes e metodologia seguem no fluxo da página.
dashboard_style.markdown(dashboard_css + f"""
<style>
    .st-key-capital-chart {{ height: calc(100dvh - 192px) !important; flex: none !important; min-height: 0; }}
    .st-key-month-chart, .st-key-profile-chart {{
        height: calc(100dvh - {330 + table_height}px) !important; flex: none !important; min-height: 0;
    }}
    @media (max-width: 900px) {{
        .st-key-capital-chart {{ height: 650px !important; }}
        .st-key-month-chart, .st-key-profile-chart {{ height: 280px !important; }}
    }}
</style>
""", unsafe_allow_html=True)

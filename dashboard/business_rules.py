"""
FASE 4: Implementação das Regras de Negócio Interseccionais (ODS 5 e ODS 18)
Aplicadas estritamente sobre o recorte dos Critérios de Inclusão e Exclusão da Equipe:
  - Janeiro a Dezembro de 2025
  - Somente Capitais do Brasil (excluindo sem município identificado)
  - Fonte Original (SINESP): Estupro, Feminicídio e Tentativa de feminicídio (Somente vítimas do sexo feminino)
  - Fonte Fogo Cruzado: Mulheres entre 18 e 45 anos (excluindo sem idade informada),
    somente Mulher cis e Mulher trans e travesti (excluindo sem gênero informado)
"""
from typing import Dict, Any
import numpy as np
import pandas as pd


def build_unified_dataset(df_sinesp: pd.DataFrame, df_fc: pd.DataFrame) -> pd.DataFrame:
    """Consolida registros mensais com pesos, sem vincular ou deduplicar pessoas entre fontes."""
    common = ["ano", "mes", "regiao", "uf"]
    official = df_sinesp[common + ["municipio", "evento", "feminino"]].rename(
        columns={"evento": "tipo_violencia", "feminino": "quantidade"}
    ).copy()
    official["genero"] = "Não informado"
    official["raca"] = "Não informado"
    official["idade"] = pd.Series(pd.NA, index=official.index, dtype="Float64")
    official["origem"] = "SINESP"
    official["situacao"] = np.where(official["tipo_violencia"] == "Feminicídio", "Morta", "Não informado")

    individual = df_fc[common + ["cidade", "genero", "raca", "idade"]].rename(
        columns={"cidade": "municipio"}
    ).copy()
    individual["tipo_violencia"] = "Violência armada"
    individual["quantidade"] = 1
    individual["idade"] = pd.to_numeric(individual["idade"], errors="coerce").astype("Float64")
    individual["origem"] = "Fogo Cruzado"
    individual["situacao"] = np.where(df_fc["is_fatal"] == 1, "Morta", "Ferida")

    base = pd.concat([official, individual], ignore_index=True)
    base["raca"] = base["raca"].replace(
        {"Não identificado": "Não informado", "Sem identificação": "Não informado", "": "Não informado"}
    ).fillna("Não informado")
    # A procedência permite auditoria; não cria divisões na interface.
    dimensions = [c for c in base.columns if c != "quantidade"]
    return base.groupby(dimensions, dropna=False, as_index=False)["quantidade"].sum()


def compute_kpi_metrics(
    df_sinesp: pd.DataFrame,
    df_fc: pd.DataFrame,
    stat_mode: str = "Média",
) -> Dict[str, Any]:
    """
    Calcula 6 KPIs analíticos chave para o recorte da equipe (Jan-Dez 2025, Capitais, Mulheres),
    com suporte ao alternador dinâmico Média vs. Mediana.
    """
    # --- Base 1: SINESP Capitais 2025 (Somente Vítimas do Sexo Feminino) ---
    total_fem_sinesp = int(df_sinesp["feminino"].sum()) if len(df_sinesp) > 0 else 0
    capitais_ativas_sinesp = int(df_sinesp["municipio"].nunique()) if len(df_sinesp) > 0 else 0

    mask_feminicidio = df_sinesp["evento"] == "Feminicídio"
    mask_tentativa = df_sinesp["evento"] == "Tentativa de feminicídio"
    mask_estupro = df_sinesp["evento"] == "Estupro"

    vit_feminicidio = int(df_sinesp.loc[mask_feminicidio, "feminino"].sum()) if len(df_sinesp) > 0 else 0
    vit_tentativa = int(df_sinesp.loc[mask_tentativa, "feminino"].sum()) if len(df_sinesp) > 0 else 0
    vit_estupro = int(df_sinesp.loc[mask_estupro, "feminino"].sum()) if len(df_sinesp) > 0 else 0

    den_fem = vit_feminicidio + vit_tentativa
    taxa_letalidade_feminicidio_pct = (
        round((vit_feminicidio / den_fem) * 100, 1) if den_fem > 0 else 0.0
    )

    # Alternador Dinâmico Média vs. Mediana de vítimas femininas por Capital (SINESP)
    if len(df_sinesp) > 0:
        cap_grouped = df_sinesp.groupby(["uf", "municipio"])["feminino"].sum()
        vit_por_capital = round(
            float(cap_grouped.mean() if stat_mode == "Média" else cap_grouped.median()), 1
        )
    else:
        vit_por_capital = 0.0

    # --- Base 2: Fogo Cruzado Capitais 2025 (Mulheres 18-45 anos: Cis e Trans/Travesti) ---
    total_mulheres_fc = len(df_fc)
    mortas_fc = int(df_fc["is_fatal"].sum()) if total_mulheres_fc > 0 else 0
    feridas_fc = total_mulheres_fc - mortas_fc
    taxa_letalidade_fc = (
        round((mortas_fc / total_mulheres_fc) * 100, 1) if total_mulheres_fc > 0 else 0.0
    )

    # Recorte de Identidade de Gênero (Mulher cis vs. Mulher trans e travesti)
    mulheres_cis_fc = int((df_fc["genero"] == "Mulher cis").sum()) if total_mulheres_fc > 0 else 0
    mulheres_trans_fc = (
        int((df_fc["genero"] == "Mulher trans e travesti").sum()) if total_mulheres_fc > 0 else 0
    )

    # Recorte Racial ODS 18 (Mulheres Negras entre as vítimas com raça identificada)
    df_raca_id = df_fc[~df_fc["raca"].isin(["Não identificado", "Sem identificação", ""])]
    mulheres_negras_fc = int((df_raca_id["raca"] == "Negra").sum()) if len(df_raca_id) > 0 else 0
    pct_negras_identificadas = (
        round((mulheres_negras_fc / len(df_raca_id)) * 100, 1) if len(df_raca_id) > 0 else 0.0
    )

    # Alternador Dinâmico Média vs. Mediana de Idade (Recorte 18-45 anos)
    idades_validas = pd.to_numeric(df_fc["idade"], errors="coerce").dropna()
    if len(idades_validas) > 0:
        idade_central = round(
            float(idades_validas.mean() if stat_mode == "Média" else idades_validas.median()), 1
        )
    else:
        idade_central = 0.0

    return {
        "total_fem_sinesp": total_fem_sinesp,
        "capitais_ativas_sinesp": capitais_ativas_sinesp,
        "vit_feminicidio": vit_feminicidio,
        "vit_tentativa": vit_tentativa,
        "vit_estupro": vit_estupro,
        "taxa_letalidade_feminicidio_pct": taxa_letalidade_feminicidio_pct,
        "vit_por_capital": vit_por_capital,
        "total_mulheres_fc": total_mulheres_fc,
        "mortas_fc": mortas_fc,
        "feridas_fc": feridas_fc,
        "taxa_letalidade_fc": taxa_letalidade_fc,
        "mulheres_cis_fc": mulheres_cis_fc,
        "mulheres_trans_fc": mulheres_trans_fc,
        "mulheres_negras_fc": mulheres_negras_fc,
        "pct_negras_identificadas": pct_negras_identificadas,
        "idade_central": idade_central,
        "stat_mode": stat_mode,
    }


def build_intersectional_matrix(
    df_fc: pd.DataFrame,
    normalize_pct: bool = False,
) -> pd.DataFrame:
    """
    Regra de Negócio Principal (Fase 4): Cruzamento Interseccional Gênero x Raça/Cor
    sobre as mulheres (18-45 anos, Mulher cis e Mulher trans e travesti) nas Capitais em 2025.
    """
    if len(df_fc) == 0:
        return pd.DataFrame()

    df_work = df_fc.copy()
    df_work["idade_num"] = pd.to_numeric(df_work["idade"], errors="coerce")

    grouped = (
        df_work.groupby(["genero", "raca"], as_index=False)
        .agg(
            total_vitimas=("is_fatal", "count"),
            total_mortos=("is_fatal", "sum"),
            acao_policial_vitimas=("acao_policial", "sum"),
            idade_media=("idade_num", "mean"),
            idade_mediana=("idade_num", "median"),
        )
    )
    grouped["total_feridos"] = grouped["total_vitimas"] - grouped["total_mortos"]
    grouped["taxa_letalidade_pct"] = np.where(
        grouped["total_vitimas"] > 0,
        (grouped["total_mortos"] / grouped["total_vitimas"] * 100).round(1),
        0.0,
    )
    grouped["pct_acao_policial"] = np.where(
        grouped["total_vitimas"] > 0,
        (grouped["acao_policial_vitimas"] / grouped["total_vitimas"] * 100).round(1),
        0.0,
    )
    total_geral = grouped["total_vitimas"].sum()
    grouped["participacao_total_pct"] = (
        (grouped["total_vitimas"] / total_geral * 100).round(2) if total_geral > 0 else 0.0
    )
    grouped["idade_media"] = grouped["idade_media"].round(1)
    grouped["idade_mediana"] = grouped["idade_mediana"].round(1)

    return grouped.sort_values("total_vitimas", ascending=False).reset_index(drop=True)


def compute_dynamic_aggregation_by_capital(
    df_sinesp: pd.DataFrame,
    stat_mode: str = "Média",
) -> pd.DataFrame:
    """
    Agrega os dados de violência contra a mulher nas Capitais do Brasil em 2025 (SINESP),
    calculando a Soma Anual e a Tendência Central Mensal (Média vs. Mediana por mês) em cada Capital.
    """
    if len(df_sinesp) == 0:
        return pd.DataFrame()

    monthly_cap = (
        df_sinesp.groupby(["regiao", "uf", "estado", "municipio", "mes"], as_index=False)
        .agg(vitimas_feminino=("feminino", "sum"))
    )

    agg_func = "mean" if stat_mode == "Média" else "median"
    cap_summary = (
        monthly_cap.groupby(["regiao", "uf", "estado", "municipio"], as_index=False)
        .agg(
            meses_com_registro=("mes", "nunique"),
            soma_vitimas_fem=("vitimas_feminino", "sum"),
            metrica_central_mensal=("vitimas_feminino", agg_func),
        )
    )

    # Detalhamento por tipo de evento na capital
    ev_pivot = (
        df_sinesp.pivot_table(
            index=["uf", "municipio"],
            columns="evento",
            values="feminino",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    for ev_col in ["Feminicídio", "Tentativa de feminicídio", "Estupro"]:
        if ev_col not in ev_pivot.columns:
            ev_pivot[ev_col] = 0

    cap_summary = cap_summary.merge(
        ev_pivot[["uf", "municipio", "Feminicídio", "Tentativa de feminicídio", "Estupro"]],
        on=["uf", "municipio"],
        how="left",
    )
    cap_summary["metrica_central_mensal"] = cap_summary["metrica_central_mensal"].round(2)
    cap_summary["taxa_consumacao_fem_pct"] = np.where(
        (cap_summary["Feminicídio"] + cap_summary["Tentativa de feminicídio"]) > 0,
        (
            cap_summary["Feminicídio"]
            / (cap_summary["Feminicídio"] + cap_summary["Tentativa de feminicídio"])
            * 100
        ).round(1),
        0.0,
    )
    return cap_summary.sort_values("soma_vitimas_fem", ascending=False).reset_index(drop=True)

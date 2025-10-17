from dash import html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from app import app

# -----------------------------
# Carregar dados
# -----------------------------
df_vendas = pd.read_csv("data/vendas.csv")
df_meta = pd.read_csv("data/meta_regional.csv")

# Normalizar nomes
df_vendas["regiao"] = df_vendas["regiao"].str.title()
df_vendas["canal_vendas"] = df_vendas["canal_vendas"].str.title()
df_meta["regiao"] = df_meta["regiao"].str.title()

# -----------------------------
# Paletas de cores
# -----------------------------
color_map_regiao = {
    "Norte": "#9467bd",
    "Nordeste": "#8c564b",
    "Centro-Oeste": "#e377c2",
    "Sudeste": "#7f7f7f",
    "Sul": "#bcbd22"
}

color_map_canal = {
    "Loja Própria": "#1f77b4",
    "Distribuidor Credenciado": "#ff7f0e",
    "Key Account 1": "#2ca02c",
    "Key Account 2": "#d62728",
    "Key Account 3": "#17becf",
    "Key Account 4": "#9467bd"
}

# -----------------------------
# Funções para formatar valores
# -----------------------------
def formatar_milhoes_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_milhoes_abreviado(valor):
    valor_milhoes = valor / 1_000_000
    return f"R$ {valor_milhoes:,.1f}M".replace(",", "X").replace(".", ",").replace("X", ".")

# -----------------------------
# Layout da página
# -----------------------------
def layout():
    return html.Div([
        html.H3("Projeção de Vendas", className="text-center mt-4 mb-4"),
        dbc.Row([
            # Filtros laterais
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Filtros", className="card-title text-primary"),
                        html.H6("Região"),
                        dcc.Checklist(
                            id="filtro-regiao-prev",
                            options=[{"label": r, "value": r} for r in sorted(df_vendas["regiao"].unique())],
                            value=sorted(df_vendas["regiao"].unique()),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        ),
                        html.H6("Canal"),
                        dcc.Checklist(
                            id="filtro-canal-prev",
                            options=[{"label": c, "value": c} for c in sorted(df_vendas["canal_vendas"].unique())],
                            value=sorted(df_vendas["canal_vendas"].unique()),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        )
                    ]),
                    style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "10px"}
                ),
                xs=12, sm=12, md=3
            ),

            # Corpo principal com abas
            dbc.Col(
                dbc.Tabs([

                    dbc.Tab(label="Painel Geral", tab_id="aba-geral", children=[
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(dbc.CardBody([
                                    html.H6("Faturamento Atual"),
                                    html.H4(id="kpi-pct-atingido", className="text-center")
                                ]), color="info", inverse=True),
                                xs=6, sm=6, md=6, className="mb-2"
                            ),
                            dbc.Col(
                                dbc.Card(dbc.CardBody([
                                    html.H6("Falta para Meta"),
                                    html.H4(id="kpi-falta-meta", className="text-center")
                                ]), color="warning", inverse=True),
                                xs=6, sm=6, md=6, className="mb-2"
                            )
                        ], className="g-2 mb-4"),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="grafico-linha-global"), xs=12, md=12)
                        ])
                    ]),

                    dbc.Tab(label="Desempenho Regional", tab_id="aba-regional", children=[
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="grafico-regional-meta"), xs=12, md=12)
                        ])
                    ]),

                    dbc.Tab(label="Top Categorias", tab_id="aba-top", children=[
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="grafico-top-categorias"), xs=12, md=12)
                        ])
                    ])
                ], id="tabs-previsao", active_tab="aba-geral"),
                xs=12, sm=12, md=9
            )
        ], className="g-4")
    ], className="container-fluid p-3")

# -----------------------------
# Callback para KPIs e gráficos
# -----------------------------
@app.callback(
    Output("kpi-pct-atingido", "children"),
    Output("kpi-falta-meta", "children"),
    Output("grafico-linha-global", "figure"),
    Output("grafico-regional-meta", "figure"),
    Output("grafico-top-categorias", "figure"),
    Input("filtro-regiao-prev", "value"),
    Input("filtro-canal-prev", "value")
)
def atualizar_dashboard(regioes_selecionadas, canais_selecionados):
    df_filtrado = df_vendas[
        df_vendas["regiao"].isin(regioes_selecionadas) &
        df_vendas["canal_vendas"].isin(canais_selecionados)
    ].copy()

    df_meta_filtrado = df_meta[
        df_meta["regiao"].isin(regioes_selecionadas) &
        df_meta["mes"].isin(df_filtrado["mes"].unique())
    ].copy()

    if df_filtrado.empty:
        return "—", "—", {}, {}, {}

    # KPI Faturamento e Falta para Meta
    df_filtrado["meta_simulada"] = df_filtrado["prev_vendas"] * 1.035
    total_vendas = df_filtrado["vendas"].sum()
    total_meta_simulada = df_filtrado["meta_simulada"].sum() if not df_filtrado.empty else 1

    kpi_atingido_fmt = formatar_milhoes_abreviado(total_vendas)
    falta_meta_valor = max(0, total_meta_simulada - total_vendas)
    falta_meta_fmt = formatar_milhoes_abreviado(falta_meta_valor)

    # Gráfico linha global
    df_global = df_filtrado.groupby("mes", as_index=False).agg(
        vendas=("vendas","sum"),
        prev_vendas=("prev_vendas","mean")
    )
    df_global = df_global.merge(
        df_meta.groupby("mes", as_index=False).agg(meta_global=("meta_global","sum")),
        on="mes", how="left"
    )
    df_global["mes_nome"] = df_global["mes"].apply(lambda x: pd.to_datetime(f"2025-{int(x)}-01").strftime("%b"))
    df_global["vendas_fmt"] = df_global["vendas"].apply(formatar_milhoes_br)
    df_global["meta_fmt"] = df_global["meta_global"].apply(lambda x: formatar_milhoes_br(x) if not pd.isna(x) else "—")
    df_global["prev_fmt"] = df_global["prev_vendas"].apply(formatar_milhoes_br)

    fig_linha_global = px.line(
        df_global, x="mes_nome", y=["vendas","meta_global","prev_vendas"],
        markers=True, labels={"value":"R$ Vendas","mes_nome":"Mês","variable":"Indicador"},
        title="Vendas Globais vs Meta e Previsão"
    )
    fig_linha_global.update_traces(
        hovertemplate="<b>%{x}</b><br>Vendas: %{customdata[0]}<br>Meta: %{customdata[1]}<br>Previsto: %{customdata[2]}",
        customdata=df_global[["vendas_fmt","meta_fmt","prev_fmt"]].values
    )

    # Gráfico regional
    df_regional = (
        df_filtrado.groupby(["regiao", "mes"], as_index=False)
        .agg(
            vendas=("vendas", "sum"),
            meta_simulada_mes=("meta_simulada", "sum")
        )
    )
    df_regional = df_regional.merge(df_meta_filtrado, on=["regiao", "mes"], how="left")
    df_regional["pct_atingido"] = np.where(
        df_regional["meta_simulada_mes"] > 0,
        (df_regional["vendas"] / df_regional["meta_simulada_mes"]) * 100,
        0
    ).round(1)
    df_regional["mes_nome"] = df_regional["mes"].apply(lambda x: pd.to_datetime(f"2025-{int(x)}-01").strftime("%b"))
    df_regional["vendas_fmt"] = df_regional["vendas"].apply(formatar_milhoes_br)
    df_regional["meta_simulada_fmt"] = df_regional["meta_simulada_mes"].apply(formatar_milhoes_br)
    df_regional["meta_regional_fmt"] = df_regional["meta_regional"].apply(lambda x: formatar_milhoes_br(x) if not pd.isna(x) else "—")
    df_regional = df_regional.sort_values(["mes", "regiao"])

    fig_regional_meta = px.bar(
        df_regional,
        x="mes_nome",
        y="vendas",
        color="regiao",
        barmode="group",
        text="pct_atingido",
        color_discrete_map=color_map_regiao,
        labels={"vendas":"Vendas","mes_nome":"Mês"},
        title="Desempenho Regional vs Meta"
    )
    fig_regional_meta.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate=(
            "<b>Região:</b> %{customdata[0]}<br>"
            "<b>Mês:</b> %{customdata[1]}<br>"
            "<b>Vendas:</b> %{customdata[2]}<br>"
            "<b>Meta (simulada):</b> %{customdata[3]}<br>"
            "<b>% Atingido:</b> %{text:.1f}%<extra></extra>"
        ),
        customdata=np.stack([
            df_regional["regiao"],
            df_regional["mes_nome"],
            df_regional["vendas_fmt"],
            df_regional["meta_simulada_fmt"]
        ], axis=-1)
    )

    # Gráfico top categorias
    df_categoria = df_filtrado.groupby("categoria_produto", as_index=False).agg(vendas=("vendas","sum"))
    df_categoria = df_categoria.sort_values("vendas", ascending=False)
    df_categoria["vendas_fmt"] = df_categoria["vendas"].apply(formatar_milhoes_br)

    fig_top_categorias = px.bar(
        df_categoria,
        x="categoria_produto",
        y="vendas",
        labels={"vendas":"Vendas","categoria_produto":"Categoria"},
        title="Top Categorias por Vendas",
        color="vendas",
        color_continuous_scale="Teal",
        hover_data={"vendas_fmt": True}
    )
    fig_top_categorias.update_traces(
        hovertemplate="Categoria: %{x}<br>Vendas: %{customdata[0]}",
        customdata=df_categoria[["vendas_fmt"]].values
    )

    return kpi_atingido_fmt, falta_meta_fmt, fig_linha_global, fig_regional_meta, fig_top_categorias


# home.py
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from app import app
import os

# -----------------------------
# Carregar dados de forma robusta (compatível com Render)
# -----------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "vendas.csv")
df = pd.read_csv(DATA_PATH)

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
    "Distribuidor": "#ff7f0e",
    "Key Account": "#2ca02c"
}

# -----------------------------
# Coordenadas fictícias das capitais (para lojas próprias)
# -----------------------------
capitais = {
    "Norte": [(-3.1, -60.0)],
    "Nordeste": [(-8.0, -35.0)],
    "Centro-Oeste": [(-15.8, -47.9)],
    "Sudeste": [(-23.5, -46.6)],
    "Sul": [(-30.0, -51.2)]
}

np.random.seed(42)
def gerar_pontos_aleatorios(regiao, n):
    lat_base, lon_base = capitais[regiao][0]
    return [(lat_base + np.random.uniform(-2, 2), lon_base + np.random.uniform(-2, 2)) for _ in range(n)]

# -----------------------------
# Adiciona lat/lon de forma segura (sem warnings)
# -----------------------------
lats, lons = [], []
for _, row in df.iterrows():
    if row["canal_vendas"] == "Loja Própria":
        lat, lon = capitais[row["regiao"]][0]
    else:
        lat, lon = gerar_pontos_aleatorios(row["regiao"], 1)[0]
    lats.append(lat)
    lons.append(lon)

df["lat"] = lats
df["lon"] = lons

# -----------------------------
# Funções de formatação
# -----------------------------
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    return f"{valor:.1f}%"

# -----------------------------
# Layout da página
# -----------------------------
def layout():
    return html.Div([

        html.H3("Painel Executivo de Vendas", className="text-center mt-4 mb-4 titulo-principal"),

        dbc.Row([
            # Coluna esquerda: filtros
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Filtros", className="card-title text-primary"),
                        html.H6("Região"),
                        dcc.Checklist(
                            id="filtro-regiao",
                            options=[{"label": r, "value": r} for r in df["regiao"].unique()],
                            value=df["regiao"].unique().tolist(),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        ),
                        html.H6("Canal"),
                        dcc.Checklist(
                            id="filtro-canal",
                            options=[{"label": c, "value": c} for c in df["canal_vendas"].unique()],
                            value=df["canal_vendas"].unique().tolist(),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        )
                    ]),
                    style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "10px"}
                )
            ], xs=12, sm=12, md=3),

            # Coluna direita: KPIs e abas
            dbc.Col([
                # KPIs
                dbc.Row([
                    dbc.Col(dbc.Card(dbc.CardBody([
                        html.H6("Vendas Totais"),
                        html.H4(id="kpi-vendas", className="text-center")
                    ]), color="info", inverse=True), xs=12, sm=12, md=4),
                    dbc.Col(dbc.Card(dbc.CardBody([
                        html.H6("Lucro Total"),
                        html.H4(id="kpi-lucro", className="text-center")
                    ]), color="success", inverse=True), xs=12, sm=12, md=4),
                    dbc.Col(dbc.Card(dbc.CardBody([
                        html.H6("Margem Média (%)"),
                        html.H4(id="kpi-margem", className="text-center")
                    ]), color="warning", inverse=True), xs=12, sm=12, md=4),
                ], className="g-3 mb-4"),

                # Abas
                dbc.Tabs([
                    dbc.Tab(label="Vendas Totais por Região", tab_id="aba-barras", children=[
                        dcc.Graph(id="grafico-barras", className="m-2")
                    ]),
                    dbc.Tab(label="Distribuição de Vendas por Canal", tab_id="aba-mapa", children=[
                        dcc.Graph(id="mapa-vendas", className="m-2")
                    ]),
                    dbc.Tab(label="Planilha de Dados", tab_id="aba-tabela", children=[
                        html.Div(id="tabela-container", className="m-2")
                    ])
                ], id="tabs-home", active_tab="aba-barras")
            ], xs=12, sm=12, md=9)
        ], className="g-4")
    ], className="container-fluid p-3")

# -----------------------------
# Callback para atualização
# -----------------------------
@app.callback(
    Output("kpi-vendas", "children"),
    Output("kpi-lucro", "children"),
    Output("kpi-margem", "children"),
    Output("grafico-barras", "figure"),
    Output("mapa-vendas", "figure"),
    Output("tabela-container", "children"),
    Input("filtro-regiao", "value"),
    Input("filtro-canal", "value")
)
def atualizar_dashboard(regioes_selecionadas, canais_selecionados):
    df_filtrado = df.loc[
        df["regiao"].isin(regioes_selecionadas) & df["canal_vendas"].isin(canais_selecionados)
    ].copy()

    # KPIs
    total_vendas = df_filtrado["vendas"].sum()
    total_lucro = df_filtrado["lucro"].sum()
    margem_media = (total_lucro / total_vendas * 100) if total_vendas != 0 else 0

    kpi_vendas = formatar_brl(total_vendas)
    kpi_lucro = formatar_brl(total_lucro)
    kpi_margem = formatar_percentual(margem_media)

    # Gráfico de barras
    df_bar = df_filtrado.groupby("regiao", as_index=False)["vendas"].sum()
    fig_bar = px.bar(
        df_bar,
        x="regiao",
        y="vendas",
        color="regiao",
        color_discrete_map=color_map_regiao,
        title="Vendas Totais por Região"
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>Vendas: %{customdata}<extra></extra>",
        customdata=[formatar_brl(v) for v in df_bar["vendas"]]
    )
    fig_bar.update_layout(
        hoverlabel=dict(bgcolor="rgba(50,50,50,0.9)", font_size=13, font_color="white"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Mapa interativo
    df_filtrado = df_filtrado.assign(
        vendas_fmt=df_filtrado["vendas"].apply(formatar_brl),
        lucro_fmt=df_filtrado["lucro"].apply(formatar_brl)
    )

    fig_map = px.scatter_geo(
        df_filtrado,
        lat="lat",
        lon="lon",
        color="canal_vendas",
        size="vendas",
        hover_name="canal_vendas",
        hover_data={
            "vendas_fmt": True,
            "lucro_fmt": True,
            "lat": False,
            "lon": False
        },
        color_discrete_map=color_map_canal,
        scope="south america",
        title="Distribuição de Vendas por Canal (Mapa do Brasil)"
    )
    fig_map.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Vendas: %{customdata[0]}<br>Lucro: %{customdata[1]}<extra></extra>",
        customdata=np.stack((df_filtrado["vendas_fmt"], df_filtrado["lucro_fmt"]), axis=-1)
    )
    fig_map.update_layout(
        hoverlabel=dict(bgcolor="rgba(50,50,50,0.9)", font_size=13, font_color="white"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Planilha de dados
    df_resumo = df_filtrado.groupby(["regiao", "canal_vendas"], as_index=False).agg(
        vendas=("vendas", "sum"),
        lucro=("lucro", "sum")
    )

    df_resumo = df_resumo.assign(
        pct_meta=df_resumo["lucro"] / (df_resumo["vendas"] * 1.10)
    )

    max_vendas = df_resumo["vendas"].max()
    max_lucro = df_resumo["lucro"].max()

    def criar_barra(valor, max_valor, cor="#1f77b4", formato="valor"):
        pct = int((valor / max_valor) * 100) if max_valor != 0 else 0
        texto = formatar_brl(valor) if formato == "valor" else f"{valor*100:.1f}%"
        return html.Div([
            html.Span(texto, className="barra-texto" + (" percentual" if formato=="percentual" else "")),
            html.Div(style={
                "width": f"{pct}%",
                "backgroundColor": cor,
                "height": "14px",
                "borderRadius": "6px",
                "marginTop": "4px"
            })
        ])

    tabela = html.Table([
        html.Thead(html.Tr([
            html.Th("Região"),
            html.Th("Canal"),
            html.Th("Vendas"),
            html.Th("Lucro"),
            html.Th("% Meta")
        ])),
        html.Tbody([
            html.Tr([
                html.Td(row["regiao"]),
                html.Td(row["canal_vendas"]),
                html.Td(criar_barra(row["vendas"], max_vendas, "#1f77b4", "valor")),
                html.Td(criar_barra(row["lucro"], max_lucro, "#2ca02c", "valor")),
                html.Td(criar_barra(row["pct_meta"], 1, "#4caf50", "percentual"))
            ]) for _, row in df_resumo.iterrows()
        ])
    ], className="tabela-customizada")

    return kpi_vendas, kpi_lucro, kpi_margem, fig_bar, fig_map, tabela

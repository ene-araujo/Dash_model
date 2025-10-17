from dash import html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from app import app

# -----------------------------
# Carregar dados
# -----------------------------
df = pd.read_csv("data/vendas.csv")

# -----------------------------
# Funções de formatação
# -----------------------------
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    return f"{valor:.1f}%"

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

# -----------------------------
# Layout da página
# -----------------------------
def layout():
    return html.Div([
        html.H3("Análise de Portfólio e Desempenho", className="text-center mt-4 mb-4"),

        dbc.Row([
            # Coluna filtros
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Filtros", className="card-title text-primary"),
                        html.H6("Região"),
                        dcc.Checklist(
                            id="filtro-regiao-analise",
                            options=[{"label": r, "value": r} for r in sorted(df["regiao"].unique())],
                            value=sorted(df["regiao"].unique()),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        ),
                        html.H6("Canal"),
                        dcc.Checklist(
                            id="filtro-canal-analise",
                            options=[{"label": c, "value": c} for c in sorted(df["canal_vendas"].unique())],
                            value=sorted(df["canal_vendas"].unique()),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        ),
                        html.H6("Produto"),
                        dcc.Checklist(
                            id="filtro-produto-analise",
                            options=[{"label": p, "value": p} for p in sorted(df["produto"].unique())],
                            value=sorted(df["produto"].unique()),
                            labelStyle={"display": "block", "margin-bottom": "5px"},
                            inputStyle={"margin-right": "10px"}
                        )
                    ]),
                    style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "10px"}
                ),
                xs=12, sm=12, md=3
            ),

            # Coluna gráficos / KPIs
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(dbc.CardBody([
                            html.H6("Alta venda / Baixa margem"),
                            html.Div(id="insight-1", className="fw-bold text-center mt-2")
                        ]), color="info", inverse=True, className="shadow-sm"), xs=12, sm=12, md=4
                    ),
                    dbc.Col(
                        dbc.Card(dbc.CardBody([
                            html.H6("Baixa venda / Alta margem"),
                            html.Div(id="insight-2", className="fw-bold text-center mt-2")
                        ]), color="warning", inverse=True, className="shadow-sm"), xs=12, sm=12, md=4
                    ),
                    dbc.Col(
                        dbc.Card(dbc.CardBody([
                            html.H6("Top 3 Produtos por Lucro"),
                            html.Div(id="insight-3", className="fw-bold text-center mt-2")
                        ]), color="success", inverse=True, className="shadow-sm"), xs=12, sm=12, md=4
                    )
                ], className="g-3 mb-4"),

                dbc.Tabs([
                    dbc.Tab(label="Lucro por Produto / Canal / Região", tab_id="aba-barra",
                            children=[dcc.Graph(id="grafico-barra-analise", className="m-2")]),
                    dbc.Tab(label="Margem x Vendas por Produto", tab_id="aba-scatter",
                            children=[dcc.Graph(id="grafico-scatter-analise", className="m-2")])
                ], id="tabs-analise", active_tab="aba-barra", className="mt-2")
            ], xs=12, sm=12, md=9)
        ], className="g-4")
    ], className="container-fluid p-3")

# -----------------------------
# Callback otimizado
# -----------------------------
@app.callback(
    Output("grafico-barra-analise", "figure"),
    Output("grafico-scatter-analise", "figure"),
    Output("insight-1", "children"),
    Output("insight-2", "children"),
    Output("insight-3", "children"),
    Input("filtro-regiao-analise", "value"),
    Input("filtro-canal-analise", "value"),
    Input("filtro-produto-analise", "value")
)
def atualizar_analise(regioes, canais, produtos):
    # Filtrar apenas uma vez
    df_filtrado = df.query(
        "regiao in @regioes and canal_vendas in @canais and produto in @produtos"
    ).copy()

    if df_filtrado.empty:
        return {}, {}, "Nenhum", "Nenhum", "Nenhum"

    # -----------------------------
    # Gráfico de barras: % da meta
    # -----------------------------
    df_bar = df_filtrado.groupby(["produto", "canal_vendas", "regiao"], as_index=False).agg(
        vendas=("vendas", "sum"),
        lucro=("lucro", "sum")
    )
    df_bar["pct_meta"] = (df_bar["lucro"] / (df_bar["vendas"] * 1.10) * 100).round(1)

    fig_bar = px.bar(
        df_bar,
        x="produto",
        y="pct_meta",
        color="regiao",
        barmode="group",
        text=df_bar.apply(lambda r: f'{formatar_brl(r.lucro)}\n{r.pct_meta}%', axis=1),
        color_discrete_map=color_map_regiao,
        title="Performance de Lucro por Produto/Canal/Região (% da Meta)"
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>Canal: %{customdata[0]}<br>Região: %{customdata[1]}<br>Lucro: %{customdata[2]}<br>Vendas: %{customdata[3]}<br>% da Meta: %{y:.1f}%",
        customdata=np.stack([
            df_bar["canal_vendas"],
            df_bar["regiao"],
            df_bar["lucro"].apply(formatar_brl),
            df_bar["vendas"].apply(formatar_brl)
        ], axis=-1),
        textposition='outside'
    )
    fig_bar.update_layout(
        yaxis_title="% da Meta",
        xaxis_title="Produto",
        legend_title="Região",
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        hoverlabel=dict(bgcolor="rgba(50,50,50,0.9)", font_size=13, font_color="white")
    )

    # -----------------------------
    # Gráfico scatter: Margem x Vendas
    # -----------------------------
    df_filtrado["margem"] = np.where(df_filtrado["vendas"] != 0, df_filtrado["lucro"] / df_filtrado["vendas"] * 100, 0)
    fig_scatter = px.scatter(
        df_filtrado,
        x="vendas",
        y="margem",
        color="regiao",
        size="vendas",
        hover_name="produto",
        hover_data={"canal_vendas": True, "regiao": True, "vendas": True, "lucro": True, "margem": True},
        color_discrete_map=color_map_regiao,
        title="Margem x Vendas por Produto"
    )
    fig_scatter.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Canal: %{customdata[0]}<br>Região: %{customdata[1]}<br>Vendas: %{customdata[2]}<br>Lucro: %{customdata[3]}<br>Margem: %{customdata[4]:.1f}%",
        customdata=np.stack([
            df_filtrado["canal_vendas"],
            df_filtrado["regiao"],
            df_filtrado["vendas"].apply(formatar_brl),
            df_filtrado["lucro"].apply(formatar_brl),
            df_filtrado["margem"]
        ], axis=-1)
    )
    fig_scatter.update_layout(
        xaxis_title="Vendas (R$)",
        yaxis_title="Margem (%)",
        hoverlabel=dict(bgcolor="rgba(50,50,50,0.9)", font_size=13, font_color="white")
    )

    # -----------------------------
    # Insights
    # -----------------------------
    df_insight = df_filtrado.groupby("produto", as_index=False).agg(vendas=("vendas", "sum"), lucro=("lucro", "sum"))
    df_insight["margem"] = np.where(df_insight["vendas"] != 0, df_insight["lucro"]/df_insight["vendas"]*100, 0)

    alta_venda_baixa_margem = df_insight[(df_insight["vendas"] > df_insight["vendas"].mean()) & (df_insight["margem"] < df_insight["margem"].mean())]["produto"].tolist()
    baixa_venda_alta_margem = df_insight[(df_insight["vendas"] < df_insight["vendas"].mean()) & (df_insight["margem"] > df_insight["margem"].mean())]["produto"].tolist()
    produtos_top = df_insight.sort_values("lucro", ascending=False)["produto"].head(3).tolist()

    return (
        fig_bar,
        fig_scatter,
        ", ".join(alta_venda_baixa_margem) if alta_venda_baixa_margem else "Nenhum",
        ", ".join(baixa_venda_alta_margem) if baixa_venda_alta_margem else "Nenhum",
        ", ".join(produtos_top) if produtos_top else "Nenhum"
    )

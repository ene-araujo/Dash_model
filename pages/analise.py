# pages/analise.py
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
from app import app

# ============================================================
# Carregamento seguro dos dados
# ============================================================

# Define caminho seguro para o Render (e também local)
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "../data/vendas.csv")

# Leitura do dataset de vendas
df = pd.read_csv(data_path)

# ============================================================
# Layout da Página de Análise
# ============================================================

def layout():
    return html.Div([
        dbc.Container([
            html.H2("📊 Análise de Desempenho de Vendas", className="text-center mb-4"),

            dbc.Row([
                dbc.Col([
                    html.Label("Selecione a Região:"),
                    dcc.Dropdown(
                        id="filtro-regiao-analise",
                        options=[{"label": r, "value": r} for r in sorted(df["Região"].unique())],
                        value=[r for r in sorted(df["Região"].unique())],
                        multi=True,
                        clearable=False
                    )
                ], width=6),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(dcc.Graph(id="grafico-vendas-por-loja"), md=6),
                dbc.Col(dcc.Graph(id="grafico-lucro-vs-meta"), md=6),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(html.Div(id="insights-analise"), width=12)
            ])
        ], fluid=True, className="p-4")
    ])

# ============================================================
# Callbacks — Geração de Gráficos e Insights
# ============================================================

@app.callback(
    Output("grafico-vendas-por-loja", "figure"),
    Output("grafico-lucro-vs-meta", "figure"),
    Output("insights-analise", "children"),
    Input("filtro-regiao-analise", "value")
)
def atualizar_graficos(regioes):
    df_filtrado = df[df["Região"].isin(regioes)].copy()

    # --- Gráfico 1: Vendas por Loja
    fig_vendas = px.bar(
        df_filtrado.groupby("Loja", as_index=False)["Vendas"].sum(),
        x="Loja", y="Vendas", color="Loja",
        title="Vendas Totais por Loja",
        text_auto=".2s"
    )
    fig_vendas.update_layout(title_x=0.5, height=400, showlegend=False)

    # --- Gráfico 2: Lucro vs Meta
    fig_lucro = px.scatter(
        df_filtrado,
        x="Lucro", y="Meta",
        color="Região", size="Vendas",
        title="Lucro x Meta por Loja",
        hover_data=["Loja"]
    )
    fig_lucro.update_layout(title_x=0.5, height=400)

    # --- Insights automáticos
    media_vendas = df_filtrado["Vendas"].mean()
    pct_meta = (df_filtrado["Lucro"].sum() / df_filtrado["Meta"].sum()) * 100

    insights = dbc.Alert(
        f"💡As lojas da(s) região(ões) selecionada(s) têm média de vendas "
        f"de R$ {media_vendas:,.0f} e atingiram {pct_meta:.1f}% da meta geral.",
        color="info",
        className="mt-3"
    )

    return fig_vendas, fig_lucro, insights

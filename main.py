# main.py
import os
from dash import html, dcc, Input, Output
from app import app, server  # IMPORTANTE: server para Gunicorn no Render
from pages import home, previsao, analise, create_navbar
import pandas as pd

# -----------------------------
# Pré-carregamento de dados (apenas uma vez)
# -----------------------------
df_vendas_global = pd.read_csv("data/vendas.csv")
df_meta_global = pd.read_csv("data/meta_regional.csv")

# -----------------------------
# Layout principal
# -----------------------------
app.layout = html.Div([
    create_navbar(),        # Navbar única
    dcc.Location(id="url"), # Controla as páginas
    html.Div(id="page-content")
])

# -----------------------------
# Callback de navegação entre páginas
# -----------------------------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    # Passa os dados já carregados para as páginas, evitando leituras repetidas
    if pathname == "/previsao":
        return previsao.layout(df_vendas=df_vendas_global, df_meta=df_meta_global)
    elif pathname == "/analise":
        return analise.layout(df_vendas=df_vendas_global)
    else:
        return home.layout(df_vendas=df_vendas_global)

# -----------------------------
# Execução do app
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)  # debug=False no Render

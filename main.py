# main.py
import os
from dash import dcc, html, Input, Output
from app import app
from pages import home, previsao, analise  # Página inicial e demais

# ==============================
# Layout principal
# ==============================
# Apenas Location e container; cada página chama sua própria navbar
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# ==============================
# Callback de navegação entre páginas
# ==============================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/previsao":
        return previsao.layout()  # Página Projeção de Vendas
    elif pathname == "/analise":
        return analise.layout()   # Página Análise de Portfólio
    else:
        return home.layout()      # Página inicial real (Home com KPIs e gráficos)

# ==============================
# Servidor
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa porta 10000 por padrão
    app.run_server(host="0.0.0.0", port=port, debug=False)

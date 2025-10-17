# main.py
import os
from dash import html, dcc, Input, Output
from app import app, server  # IMPORTANTE: server para Gunicorn no Render
from pages import home, previsao, analise, create_navbar

# Layout principal
app.layout = html.Div([
    create_navbar(),        # Barra de navegação
    dcc.Location(id="url"), # Controla as páginas
    html.Div(id="page-content")
])

# Callback de navegação
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/previsao":
        return previsao.layout()
    elif pathname == "/analise":
        return analise.layout()
    else:
        return home.layout()

# Apenas para testes locais
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)

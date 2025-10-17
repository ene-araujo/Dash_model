# main.py
import os
from dash import html, dcc, Input, Output
from app import app  # app já com Bootstrap e server definido
from pages import home, previsao, analise, create_navbar

# Layout principal
app.layout = html.Div([
    create_navbar(),        # Barra de navegação global
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
        return previsao.layout()   # chama a função layout()
    elif pathname == "/analise":
        return analise.layout()    # chama a função layout()
    else:
        return home.layout()       # página inicial (fallback)

# Apenas para testes locais e deploy no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))       # porta dinâmica do Render
    debug = os.environ.get("DEBUG", "True").lower() in ["true", "1"]  # debug opcional
    app.run_server(host="0.0.0.0", port=port, debug=debug)

# main.py
import os
from dash import dcc, html, Input, Output
from app import app
from pages import index, previsao, analise  # importa a página inicial e as demais

# Layout principal (somente Location e container da página)
app.layout = html.Div([
    dcc.Location(id="url"),  # controla a URL
    html.Div(id="page-content")  # container onde o layout da página será renderizado
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
    else:  # Página inicial
        return index.layout()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa 10000 por padrão
    app.run_server(host="0.0.0.0", port=port)

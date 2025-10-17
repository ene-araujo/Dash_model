# main.py
import os
from dash import html, dcc, Input, Output
from app import app, server  # server é importante para Render
from pages import home, previsao, analise, create_navbar

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # controla a página
    html.Div(id="navbar-container"),       # navbar será renderizada dinamicamente
    html.Div(id="page-content")            # conteúdo das páginas
])

# Callback para atualizar navbar e página
@app.callback(
    Output("navbar-container", "children"),
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    # Atualiza navbar com a aba ativa
    navbar = create_navbar(active_path=pathname)

    # Seleciona o layout da página
    if pathname == "/previsao":
        page = previsao.layout()
    elif pathname == "/analise":
        page = analise.layout()
    else:
        page = home.layout()

    return navbar, page

# Apenas para testes locais
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)

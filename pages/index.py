from dash import html
from . import create_navbar  # importa a função do __init__.py

# Layout da página inicial
def layout():
    return html.Div([
        create_navbar(),
        html.Div(
            [
                html.H1("Página Inicial"),
                html.P("Bem-vindo ao Painel de Vendas!"),
                html.P("Use a navegação acima para acessar Previsão e Análise."),
            ],
            style={"padding": "20px"}
        )
    ])

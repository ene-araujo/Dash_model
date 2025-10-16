# pages/index.py
from dash import html
import dash_bootstrap_components as dbc

# Navbar compartilhada
def create_navbar():
    navbar = dbc.NavbarSimple(
        brand="Painel de Vendas",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Previsão", href="/previsao")),
            dbc.NavItem(dbc.NavLink("Análise", href="/analise")),
        ],
    )
    return navbar

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

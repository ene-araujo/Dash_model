from dash import html
import dash_bootstrap_components as dbc
from . import home, previsao, analise  # importa os módulos das páginas

# Função compartilhada para criar a Navbar
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


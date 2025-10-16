# pages/create_navbar.py
from dash import html
import dash_bootstrap_components as dbc

def create_navbar():
    """
    Cria a barra de navegação principal do Painel de Vendas.
    """
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

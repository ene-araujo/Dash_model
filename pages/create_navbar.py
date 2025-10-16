# pages/create_navbar.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_navbar(active_path="/"):
    """
    Cria a barra de navegação com o item ativo destacado.
    """
    # Define qual aba está ativa
    def nav_link(label, href):
        is_active = "active" if href == active_path else ""
        return dbc.NavItem(
            dbc.NavLink(label, href=href, className=f"fw-semibold {is_active}")
        )

    navbar = dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="/assets/logo.png", height="40px")),  # opcional
                    dbc.Col(dbc.NavbarBrand("Painel de Previsão de Vendas", className="ms-2"))
                ], align="center", className="g-0"),
                href="/",
                style={"textDecoration": "none"}
            ),
            dbc.Nav(
                [
                    nav_link("🏠 Home", "/"),
                    nav_link("📊 Previsão", "/previsao"),
                    nav_link("📈 Análise", "/analise")
                ],
                pills=True,
                className="ms-auto"
            ),
        ]),
        color="dark",
        dark=True,
        sticky="top",
        className="mb-4 shadow-sm"
    )

    return navbar

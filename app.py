# app.py
import dash
import dash_bootstrap_components as dbc

# Inicializa o app com tema visual do Bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="Painel de Vendas"
)

# Exponha o servidor para deploy futuro (Render, Railway, etc.)
server = app.server

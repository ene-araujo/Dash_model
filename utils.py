# utils.py
import pandas as pd

# -----------------------------
# Carregar dados
# -----------------------------
def carregar_dados(caminho="data/vendas.csv"):
    """Carrega os dados de vendas a partir do CSV."""
    return pd.read_csv(caminho)

# -----------------------------
# Formatar valores monetários
# -----------------------------
def formatar_moeda(valor):
    """Formata valores no padrão brasileiro ex: R$ 1.234.567,89"""
    if pd.isna(valor):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# -----------------------------
# Criar Tooltip (Bootstrap)
# -----------------------------
from dash import html
import dash_bootstrap_components as dbc

def criar_tooltip(target_id, texto):
    """Cria tooltips estilizados para cards e KPIs."""
    return dbc.Tooltip(
        texto,
        target=target_id,
        placement="top",
        style={
            "backgroundColor": "#343a40",
            "color": "white",
            "fontSize": "0.9rem",
            "borderRadius": "5px",
            "padding": "6px 8px"
        }
    )

#load_data.py
import pandas as pd
import os

def load_data():
    """
    Carrega os dados principais de vendas e metas regionais.
    Retorna um DataFrame único com merge por 'regiao'.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    vendas_path = os.path.join(base_dir, "vendas.csv")
    metas_path = os.path.join(base_dir, "meta_regional.csv")

    # ------------------------------
    # Verificações de existência
    # ------------------------------
    if not os.path.exists(vendas_path):
        raise FileNotFoundError(f"❌ Arquivo de vendas não encontrado: {vendas_path}")

    if not os.path.exists(metas_path):
        print("⚠️ Aviso: 'meta_regional.csv' não encontrado. Carregando apenas vendas.")
        df_vendas = pd.read_csv(vendas_path)
        return df_vendas

    # ------------------------------
    # Leitura dos arquivos
    # ------------------------------
    df_vendas = pd.read_csv(vendas_path)
    df_meta = pd.read_csv(metas_path)

    # ------------------------------
    # Normalização dos nomes de região
    # ------------------------------
    df_vendas["regiao_norm"] = df_vendas["regiao"].str.strip().str.title()
    df_meta["regiao_norm"] = df_meta["regiao"].str.strip().str.title()

    # ------------------------------
    # Merge das metas regionais
    # ------------------------------
    df_merged = df_vendas.merge(df_meta, on="regiao_norm", how="left")

    # ------------------------------
    # Limpeza final
    # ------------------------------
    df_merged.drop(columns=["regiao_norm"], inplace=True)
    
     
    # Retorna o dataset unificado
    return df_merged

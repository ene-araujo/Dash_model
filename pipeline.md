# **Painel de Previsão de Vendas – Dash + Machine Learning**

## **Visão Geral**

Este projeto consiste em um painel interativo desenvolvido em **Dash (Python)** para:

* Prever vendas futuras de produtos por região e canal.
* Comparar resultados com metas simuladas.
* Gerar KPIs e insights operacionais.
* Analisar portfólio e desempenho dos produtos.

Ele combina **Machine Learning + Visualização de Dados + Design com Bootstrap**, sendo ideal para portfólio técnico.

---

## **Estrutura do Projeto**

```text
Dash_model/
│
├── main.py                # Inicializa o app e a navbar
├── app.py                 # Configuração do Dash e tema
├── data/
│   └── vendas.csv          # Dados simulados de vendas
├── pages/
│   ├── __init__.py
│   ├── home.py             # Painel Executivo
│   ├── previsao.py         # Previsão de Vendas
│   └── analise.py          # Análise de Portfólio e Insights
└── assets/
    └── main.css           # Estilo customizado
```

---

## **Instalação e Execução**

1. Criar ambiente virtual:

```bash
python -m venv venv_dash
venv_dash\Scripts\activate   # Windows
source venv_dash/bin/activate  # Linux / macOS
```

2. Instalar dependências:

```bash
pip install dash dash-bootstrap-components plotly pandas scikit-learn joblib
```

3. Executar o app:

```bash
python main.py
```

4. Abrir navegador e acessar:

```
http://127.0.0.1:8050/
```

---

## **Funcionalidades Principais**

### **Home**

* KPIs de vendas, lucro e margem.
* Gráficos por região e canal.
* Planilha de dados interativa.

### **Previsão**

* Inputs de parâmetros de vendas.
* Previsão usando modelo ML.
* Comparativo Previsão vs Meta com gráficos dinâmicos.

### **Análise**

* Performance de produtos por canal e região.
* Scatter plot de Margem x Vendas.
* Cards de insight: produtos estratégicos, alta venda/baixa margem, baixa venda/alta margem.

---

## **Tecnologias Utilizadas**

* Python 3.11+
* Dash / Plotly
* Pandas / NumPy
* Scikit-learn
* Bootstrap (tema FLATLY)

---

## **Boas Práticas Aplicadas**

* Evitar `SettingWithCopyWarning` usando `.copy()` ou `.loc[]`.
* Funções de formatação monetária e percentual.
* Layout responsivo com `dbc.Row` e `dbc.Col`.
* Tooltips padronizados em todos os gráficos.
* Cards de KPI e insight para destaque visual.

---

## **Possíveis Expansões**

* Upload de CSV com dados reais.
* Histórico de previsões.
* Dashboards multi-ano ou multi-produto.
* Treemap ou heatmap para análise de portfólio.

---

## **Imagem do Painel**

*(Inserir aqui um screenshot do dashboard final)*

[Painel de Previsão de Vendas](assets/preview.png)
---

## **Autor**

Ananias Araujo — Outubro de 2025
Projeto para portfólio técnico público.
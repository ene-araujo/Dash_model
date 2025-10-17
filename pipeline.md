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
│   ├── vendas.csv          # Dados simulados de vendas
│   └── meta_regional.csv   # Metas regionais
├── modelos/
│   └── modelo_vendas.pkl  # Modelo de ML treinado
├── pages/
│   ├── __init__.py
│   ├── home.py             # Painel Executivo
│   ├── previsao.py         # Previsão de Vendas
│   └── analise.py          # Análise de Portfólio e Insights
└── assets/
    └── main.css           # Estilo customizado (Bootstrap Flatly)
````

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
* Planilha de dados interativa com barras de progresso e percentuais.

### **Previsão**

* Filtros de região e canal.
* Previsão usando modelo ML serializado (`.pkl`).
* Comparativo Previsão vs Meta com gráficos de linha e barras.
* KPIs de percentual atingido e valor restante para meta.

### **Análise**

* Performance de produtos por canal e região.
* Scatter plot de Margem x Vendas.
* Cards de insight:

  * Produtos com alta venda e baixa margem
  * Produtos com baixa venda e alta margem
  * Top 3 produtos por lucro

---

## **Tecnologias Utilizadas**

* Python 3.11+
* Dash / Plotly
* Pandas / NumPy
* Scikit-learn
* Bootstrap (tema FLATLY)
* Joblib (serialização de modelo)

---

## **Boas Práticas Aplicadas**

* Evitar `SettingWithCopyWarning` usando `.copy()` ou `.loc[]`.
* Funções de formatação monetária e percentual padronizadas.
* Layout responsivo com `dbc.Row` e `dbc.Col`.
* Tooltips interativos em todos os gráficos.
* Cards de KPI e insight para destaque visual.
* Estrutura de pastas limpa e modular (separação de pages, data e modelos).

---

## **Possíveis Expansões**

* Upload de CSV com dados reais.
* Histórico de previsões com armazenamento local.
* Dashboards multi-ano ou multi-produto.
* Visualizações adicionais: treemap ou heatmap para análise de portfólio.

---

## **Imagem do Painel**

![Painel de Previsão de Vendas](assets/preview.png)

---

## **Autor**

**Ananias Araujo — Outubro de 2025**
Projeto desenvolvido para portfólio técnico público.

from pathlib import Path
import pandas as pd
import plotly.express as px

caminho_arquivo = Path(__file__).resolve().parent / "Indicador_Producao.xlsx"

try:
    df = pd.read_excel(caminho_arquivo, engine="openpyxl")
    print("Planilha lida com sucesso!")
    print(df.head())

    if "categoria" in df.columns and "vendas" in df.columns:
        dados = df.groupby("categoria", as_index=False)["producao"].sum()
        print(dados)

        fig = px.bar(dados, x="produto", y="Qtd_Produzida", title="Produção por produto") 
        fig.show()
    else:
        print("As colunas 'categoria' e 'producao' não foram encontradas na planilha.")
except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho_arquivo}")
except Exception as e:
    print(f"Erro ao ler a planilha: {e}")

import pandas as pd
import  plotly.express as px


df = pd.read_csv("vendas.csv")

dados = df.groupby("categoria", as_index=False)["vendas"].sum()
print(dados)
fig = px.bar(dados, x="categoria", y="vendas", title="Vendas por categoria")
fig.show()
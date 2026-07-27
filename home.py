from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

caminho_arquivo = Path(__file__).resolve().parent / "Indicador_Producao.xlsx"

caminho_grafico = Path(__file__).resolve().parent / "grafico_producao.html"

def normalizar_colunas(df):
    df = df.copy()
    df.columns = [
        str(col).strip().lower().replace(" ", "_").replace("-", "_")
        for col in df.columns
    ]
    return df

try:
    
    df = pd.read_excel(caminho_arquivo, engine="openpyxl")
    print("Planilha lida com sucesso!")

    
    df = normalizar_colunas(df)
    print("Colunas encontradas:")
    print(df.columns.tolist())

   
    col_categoria = next((c for c in ["categoria", "grupo", "setor", "departamento"] if c in df.columns), None)
    col_qtd = next((c for c in ["qtd_produzida", "qtd", "quantidade", "producao", "produzido"] if c in df.columns), None)
    col_meta = next((c for c in ["meta_producao", "meta", "meta_produção"] if c in df.columns), None)

    
    if col_categoria is None:
        df["categoria"] = "Geral"
        col_categoria = "categoria"

  
    if col_qtd is None or col_meta is None:
        raise ValueError("Não encontrei as colunas Qtd_Produzida e Meta_Producao na planilha.")

    
    df[col_qtd] = pd.to_numeric(df[col_qtd], errors="coerce")
    df[col_meta] = pd.to_numeric(df[col_meta], errors="coerce")

    df = df.dropna(subset=[col_categoria, col_qtd, col_meta])

    dados = (
        df.groupby(col_categoria, as_index=False)
        .agg({col_qtd: "sum", col_meta: "sum"})
        .rename(columns={col_qtd: "Qtd_Produzida", col_meta: "Meta_Producao"})
    )

    print("Resumo dos dados:")
    print(dados)

    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dados[col_categoria],
        y=dados["Qtd_Produzida"],
        name="Qtd_Produzida",
        marker_color="royalblue"
    ))

    fig.add_trace(go.Bar(
        x=dados[col_categoria],
        y=dados["Meta_Producao"],
        name="Meta_Producao",
        marker_color="tomato"
    ))

    fig.update_layout(
        title="Comparação entre Produção e Meta",
        xaxis_title=col_categoria,
        yaxis_title="Qtd_Total",
        barmode="group"
    )

    fig.show()

    fig.write_html(caminho_grafico)
    print(f"Gráfico salvo em: {caminho_grafico}")

except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho_arquivo}")
except Exception as e:
    print(f"Erro ao processar a planilha: {e}")
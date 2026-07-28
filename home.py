from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


PASTA_ATUAL = Path(__file__).resolve().parent
ARQUIVO_PADRAO = PASTA_ATUAL / "Indicador_Producao.xlsx"
GRAFICO_SAIDA = PASTA_ATUAL / "grafico_producao.html"

COLUNAS_CATEGORIA = ["categoria", "turno", "produto", "linha"]
COLUNAS_PRODUZIDO = ["qtd_produzida", "qtd", "quantidade", "producao", "produzido"]
COLUNAS_META = ["meta_producao", "meta", "meta_produção"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("indicador_producao")


def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        str(col).strip().lower().replace(" ", "_").replace("-", "_")
        for col in df.columns
    ]
    return df


def encontrar_coluna(df: pd.DataFrame, possiveis_nomes: list[str]) -> str | None:
    return next((nome for nome in possiveis_nomes if nome in df.columns), None)


def carregar_dados(caminho_arquivo: Path) -> pd.DataFrame:
    """Lê e normaliza a planilha de produção."""
    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    df = pd.read_excel(caminho_arquivo, engine="openpyxl")
    log.info("Planilha lida com sucesso (%d linhas).", len(df))
    return normalizar_colunas(df)


def montar_resumo(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    coluna_categoria = encontrar_coluna(df, COLUNAS_CATEGORIA)
    coluna_qtd = encontrar_coluna(df, COLUNAS_PRODUZIDO)
    coluna_meta = encontrar_coluna(df, COLUNAS_META)

    if coluna_qtd is None or coluna_meta is None:
        raise ValueError(
            "Não encontrei as colunas de quantidade produzida e/ou meta na planilha. "
            f"Colunas disponíveis: {df.columns.tolist()}"
        )

    if coluna_categoria is None:
        log.warning("Nenhuma coluna de categoria encontrada — agrupando tudo como 'Geral'.")
        df = df.assign(categoria="Geral")
        coluna_categoria = "categoria"

    df[coluna_qtd] = pd.to_numeric(df[coluna_qtd], errors="coerce")
    df[coluna_meta] = pd.to_numeric(df[coluna_meta], errors="coerce")

    linhas_antes = len(df)
    df = df.dropna(subset=[coluna_categoria, coluna_qtd, coluna_meta])
    if len(df) < linhas_antes:
        log.warning("%d linha(s) descartada(s) por dados inválidos ou incompletos.", linhas_antes - len(df))

    resumo = (
        df.groupby(coluna_categoria, as_index=False)
        .agg({coluna_qtd: "sum", coluna_meta: "sum"})
        .rename(columns={coluna_qtd: "qtd_produzida", coluna_meta: "meta_producao"})
    )

    resumo["atingimento_%"] = (
        (resumo["qtd_produzida"] / resumo["meta_producao"] * 100)
        .round(1)
        .fillna(0)
    )

    return resumo, coluna_categoria


def gerar_grafico(resumo: pd.DataFrame, coluna_categoria: str, caminho_saida: Path) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=resumo[coluna_categoria],
            y=resumo["qtd_produzida"],
            name="Produzido",
            marker_color="royalblue",
            text=resumo["qtd_produzida"],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=resumo[coluna_categoria],
            y=resumo["meta_producao"],
            name="Meta",
            marker_color="tomato",
            text=resumo["meta_producao"],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Produção Realizada x Meta",
        xaxis_title=coluna_categoria.replace("_", " ").title(),
        yaxis_title="Quantidade",
        barmode="group",
        template="plotly_white",
        legend_title="Indicador",
    )

    fig.write_html(caminho_saida)
    log.info("Gráfico salvo em: %s", caminho_saida)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera um indicador de produção a partir de uma planilha Excel.")
    parser.add_argument(
        "--arquivo",
        type=Path,
        default=ARQUIVO_PADRAO,
        help="Caminho da planilha de entrada (padrão: Indicador_Producao.xlsx na mesma pasta).",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=GRAFICO_SAIDA,
        help="Caminho do arquivo HTML de saída para o gráfico.",
    )
    args = parser.parse_args()

    try:
        df = carregar_dados(args.arquivo)
        resumo, coluna_categoria = montar_resumo(df)

        log.info("Resumo por %s:\n%s", coluna_categoria, resumo.to_string(index=False))

        gerar_grafico(resumo, coluna_categoria, args.saida)

    except FileNotFoundError as erro:
        log.error(erro)
    except ValueError as erro:
        log.error(erro)
    except Exception:
        log.exception("Erro inesperado ao processar a planilha.")


if __name__ == "__main__":
    main()

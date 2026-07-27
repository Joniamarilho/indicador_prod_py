# 📊 Análise Básica de Indicadores com Python

Este projeto consiste em uma análise exploratória e tratamento de dados de vendas utilizando **Python** e as bibliotecas **Pandas**, **Matplotlib** e **Seaborn**. O objetivo principal é transformar dados brutos de transações em *insights* visuais e estratégicos para suporte na tomada de decisão.

---

## 🎯 Objetivo

Analisar um conjunto de dados de produção, identificar padrões, tratar inconsistências e apresentar os principais indicadores de desempenho (KPIs) de forma organizada e visual.

---

## 🛠️ Etapas do Projeto

O script executa o fluxo completo de análise de dados:

1. **Importação:** Carga da base de dados de produção.
2. **Exploração Inicial:** Inspeção dos tipos de dados, formato das colunas e estrutura geral.
3. **Tratamento de Dados:** Identificação e limpeza de valores ausentes ou inconsistentes.
4. **Cálculos e Métricas:**
   - Faturamento total e ticket médio.
   - Volume de produçãp por produto (o que atingiu ou não a meta).
   - Evolução de produção entre turnos.
5. **Visualização:** Criação de gráficos claros para facilitar a leitura dos resultados.
6. **Conclusão:** Apresentação de relatórios e *insights* baseados na análise.

---

## 📋 Estrutura da Base de Dados

A base de dados requerida (ou gerada para testes) possui a seguinte estrutura mínima:

| Coluna | Descrição | Exemplo |
| :--- | :--- | :--- |
| `Data` | Data da transação comercial | `2026-03-15` |
| `Produto` | Nome do produto vendido | `Notebook` |
| `Categoria` | Categoria na qual o produto se enquadra | `Eletrônicos` |
| `Região` | Região onde a venda foi realizada | `Sudeste` |
| `Quantidade` | Número de unidades vendidas | `5` |
| `Preço Unitário` | Valor unitário do item (R$) | `3500.00` |
| `Valor Total` | Faturamento bruto da transação (`Quantidade × Preço Unitário`) | `17500.00` |

---

## 📦 Tecnologias Utilizadas

- **Python 3.x**
- **Pandas:** Manipulação e limpeza dos dados.
- **Matplotlib & Seaborn:** Visualização de dados e geração de gráficos.

---

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/analise-vendas-python.git](https://github.com/seu-usuario/analise-vendas-python.git)
   cd analise-vendas-python
   pip install pandas matplotlib seaborn
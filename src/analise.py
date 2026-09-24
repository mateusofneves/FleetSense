import pandas as pd

def analisar_locacoes(df):
    quantidade = len(df)
    media = df["dias_locacao"].mean()
    mediana = df["dias_locacao"].median()
    desvio_padrao = df["dias_locacao"].std()

    return {
        "quantidade": quantidade,
        "media": media,
        "mediana": mediana,
        "desvio_padrao": desvio_padrao
    }

def analisar_por_categoria(df):
    resultados = {}
    categorias = df['categoria'].unique()

    for categoria in categorias:
        df_categoria = df[df['categoria'] == categoria]
        resultados[categoria] = analisar_locacoes(df_categoria)

    return resultados
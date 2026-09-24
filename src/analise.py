import pandas as pd

def analisar_locacoes(df):
    quantidade = len(df)
    media = df['dias_locacao'].mean()
    mediana = df['dias_locacao'].median()
    desvio_padrao = df['dias_locacao'].std()
    minimo = df['dias_locacao'].min()
    maximo = df['dias_locacao'].max()

    return{
        'quantidade': quantidade,
        'media': media,
        'mediana': mediana,
        'desvio_padrao': desvio_padrao,
        'minimo': minimo,
        'maximo': maximo
    }

def analisar_por_categoria(df):
    resultados = {}
    categorias = df['categoria'].unique()

    for categoria in categorias:
        df_categoria = df[df['categoria'] == categoria]
        resultados[categoria] = analisar_locacoes(df_categoria)

    return resultados
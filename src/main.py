import pandas as pd
from analise import analisar_locacoes, analisar_por_categoria
from estatistica import teste_media
from estatistica import calcular_estatisticas

df = pd.read_csv('../data/locacoes.csv')

resultados = analisar_locacoes(df)

print("Quantidade de locações:", resultados['quantidade'])
print("Média de dias de locação:", resultados['media'])
print("Mediana de dias de locação:", resultados['mediana'])
print("Desvio padrão de dias de locação:", resultados['desvio_padrao'])
print("Mínimo de dias de locação:", resultados['minimo'])
print("Máximo de dias de locação:", resultados['maximo'])

media_referencia = 7

teste = teste_media(
    df['dias_locacao'], 
    media_referencia
)

print("\nTeste de hipótese")
print("t:", teste["t_statistic"])
print("p-valor:", teste["p_value"])

analise_categoria = analisar_por_categoria(df)
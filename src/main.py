import pandas as pd
from analise import analisar_locacoes

df = pd.read_csv('../data/locacoes.csv')

resultados = analisar_locacoes(df)

print("Quantidade de locações:", resultados['quantidade'])
print("Média de dias de locação:", resultados['media'])
print("Mediana de dias de locação:", resultados['mediana'])
print("Desvio padrão de dias de locação:", resultados['desvio_padrao'])
print("Mínimo de dias de locação:", resultados['minimo'])
print("Máximo de dias de locação:", resultados['maximo'])
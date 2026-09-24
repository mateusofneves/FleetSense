import pandas as pd

from analise import analisar_locacoes
from estatistica import teste_media

df = pd.read_csv("../data/locacoes.csv")

analise = analisar_locacoes(df)

media_referencia = 7

resultado = teste_media(
    df["dias_locacao"],
    media_referencia
)

print("===== FLEETSENSE =====")
print(f"Contratos: {analise['quantidade']}")
print(f"Média: {analise['media']:.2f} dias")
print(f"Mediana: {analise['mediana']:.2f} dias")
print(f"Desvio padrão: {analise['desvio_padrao']:.2f} dias")

print("\n===== TESTE DE HIPÓTESE =====")
print("H0: μ = 7 dias")
print("H1: μ ≠ 7 dias")
print(f"t: {resultado['t_statistic']:.4f}")
print(f"p-valor: {resultado['p_value']:.4f}")
print(f"α: {resultado['alpha']}")

print(f"\nDecisão: {resultado['decisao']}")

print(
    f"IC 95%: {resultado['ic_inferior']:.2f} a "
    f"{resultado['ic_superior']:.2f} dias"
)

print("\n===== CONCLUSÃO =====")
print(resultado["conclusao"])
# INTEGRANTES :

Mateus de Oliveira Fernandes Neves	572431

Olavo Dadario Vianna Barreto	569272

Paulo Henrique Lira Bilac de Araujo	569496

Pedro Soares de Souza	571285

Jhon Cutile Titirico	571976

# FleetSense

Sistema em Python para análise estatística de locações de veículos.

O FleetSense utiliza dados de contratos de locação para verificar, por meio de um teste de hipótese, se a duração média das locações é estatisticamente diferente de uma média de referência de **7 dias**.

## Objetivo

Auxiliar uma empresa de locação de veículos na análise do comportamento da duração das locações, utilizando **Inferência Estatística** para avaliar se a média observada difere de um valor de referência.

## Problema

Considerando que a empresa utiliza **7 dias** como duração média de referência, busca-se responder:

> A duração média das locações é estatisticamente diferente de 7 dias?

## Hipóteses

- **H₀:** μ = 7 dias
- **H₁:** μ ≠ 7 dias

Nível de significância:

- **α = 0,05**

## Metodologia

Foi utilizado o **teste t de uma amostra**, adequado para verificar se a média de uma amostra difere de uma média de referência quando o desvio padrão populacional é desconhecido.

O projeto também calcula:

- Quantidade de contratos
- Média das locações
- Mediana
- Desvio padrão amostral
- Estatística t
- p-valor
- Intervalo de confiança de 95%
- Decisão do teste
- Conclusão interpretável

### Regra de decisão

- Se **p-valor < 0,05** → rejeitar H₀
- Se **p-valor ≥ 0,05** → não rejeitar H₀

## Tecnologias

- Python
- Pandas
- NumPy
- SciPy
- Streamlit

## Estrutura do projeto

```text
FleetSense/
├── data/
│   └── locacoes.csv
├── src/
│   ├── main.py
│   ├── analise.py
│   ├── estatistica.py
│   └── app.py
├── README.md
├── requirements.txt
└── .gitignore

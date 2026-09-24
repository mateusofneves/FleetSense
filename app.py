import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp, t
from pathlib import Path


# ============================================================
# FLEETSENSE - DASHBOARD
# ============================================================

st.set_page_config(
    page_title="FleetSense | Dashboard",
    page_icon="🚗",
    layout="wide",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

POSSIVEIS_CAMINHOS = [
    BASE_DIR / "data" / "locacoes.csv",
    BASE_DIR.parent / "data" / "locacoes.csv",
    BASE_DIR / "locacoes.csv",
    BASE_DIR.parent / "locacoes.csv",
]

DATA_PATH = next(
    (caminho for caminho in POSSIVEIS_CAMINHOS if caminho.exists()),
    None,
)


# ============================================================
# DADOS DE DEMONSTRAÇÃO
# ============================================================

def criar_dados_demo():
    np.random.seed(42)

    categorias = [
        "Econômico",
        "SUV",
        "Sedan",
        "Luxo",
    ]

    modelos = {
        "Econômico": [
            "Fiat Mobi",
            "Renault Kwid",
            "Chevrolet Onix",
        ],
        "SUV": [
            "Jeep Renegade",
            "VW T-Cross",
            "Hyundai Creta",
        ],
        "Sedan": [
            "Toyota Corolla",
            "Honda Civic",
            "VW Virtus",
        ],
        "Luxo": [
            "BMW 320i",
            "Mercedes C180",
            "Audi A4",
        ],
    }

    registros = []

    id_locacao = 1

    for categoria in categorias:

        for modelo in modelos[categoria]:

            for _ in range(25):

                dias = max(
                    1,
                    int(round(np.random.normal(7, 3)))
                )

                registros.append(
                    {
                        "id_locacao": id_locacao,
                        "categoria": categoria,
                        "modelo": modelo,
                        "dias_locacao": dias,
                    }
                )

                id_locacao += 1

    return pd.DataFrame(registros)


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data
def carregar_dados():

    if DATA_PATH is not None:

        try:

            df = pd.read_csv(DATA_PATH)

            df["categoria"] = df["categoria"].astype(str)

            df["modelo"] = df["modelo"].astype(str)

            df["dias_locacao"] = pd.to_numeric(
                df["dias_locacao"],
                errors="coerce",
            )

            df = df.dropna(
                subset=["dias_locacao"]
            )

            return df, False

        except Exception:
            pass

    # Caso o CSV não exista ou esteja com problema,
    # usamos dados de demonstração.
    return criar_dados_demo(), True


df, usando_demo = carregar_dados()


# ============================================================
# VALIDAÇÃO
# ============================================================

colunas_obrigatorias = [
    "categoria",
    "modelo",
    "dias_locacao",
]

colunas_faltando = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in df.columns
]

if colunas_faltando:

    st.error(
        "O arquivo locacoes.csv não possui as colunas necessárias: "
        + ", ".join(colunas_faltando)
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚗 FleetSense")

st.sidebar.caption(
    "Dashboard de análise de locações"
)

st.sidebar.divider()


if usando_demo:

    st.sidebar.warning(
        "⚠️ Dados de demonstração"
    )

    st.sidebar.caption(
        "O arquivo locacoes.csv não foi encontrado. "
        "O dashboard está usando dados fictícios para demonstração."
    )

else:

    st.sidebar.success(
        "✅ Dados reais carregados"
    )


# ============================================================
# FILTROS
# ============================================================

categorias = sorted(
    df["categoria"].unique()
)

modelos = sorted(
    df["modelo"].unique()
)


categorias_selecionadas = st.sidebar.multiselect(
    "Categoria",
    categorias,
    default=categorias,
)


modelos_selecionados = st.sidebar.multiselect(
    "Modelo",
    modelos,
    default=modelos,
)


min_dias = int(
    df["dias_locacao"].min()
)

max_dias = int(
    df["dias_locacao"].max()
)


if min_dias == max_dias:

    faixa_dias = (
        min_dias,
        max_dias,
    )

else:

    faixa_dias = st.sidebar.slider(
        "Duração da locação (dias)",
        min_value=min_dias,
        max_value=max_dias,
        value=(min_dias, max_dias),
    )


# ============================================================
# FILTRAGEM
# ============================================================

df_filtrado = df[
    df["categoria"].isin(
        categorias_selecionadas
    )
    &
    df["modelo"].isin(
        modelos_selecionados
    )
    &
    df["dias_locacao"].between(
        faixa_dias[0],
        faixa_dias[1],
    )
].copy()


if df_filtrado.empty:

    st.warning(
        "Nenhum registro encontrado com os filtros selecionados."
    )

    st.stop()


# ============================================================
# ESTATÍSTICA
# ============================================================

MEDIA_REFERENCIA = 7
ALPHA = 0.05


n = len(df)

media = df["dias_locacao"].mean()

mediana = df["dias_locacao"].median()

desvio = df["dias_locacao"].std()


teste = ttest_1samp(
    df["dias_locacao"],
    MEDIA_REFERENCIA,
)


t_stat = float(
    teste.statistic
)

p_value = float(
    teste.pvalue
)


erro_padrao = desvio / np.sqrt(n)


margem = (
    t.ppf(
        1 - ALPHA / 2,
        df=n - 1,
    )
    * erro_padrao
)


ic_inferior = media - margem

ic_superior = media + margem


if p_value < ALPHA:

    decisao = "Rejeitar H₀"

    conclusao = (
        f"A duração média observada "
        f"({media:.2f} dias) é estatisticamente "
        f"diferente de {MEDIA_REFERENCIA} dias."
    )

else:

    decisao = "Não rejeitar H₀"

    conclusao = (
        f"Não há evidências estatísticas suficientes "
        f"para afirmar que a duração média "
        f"({media:.2f} dias) seja diferente de "
        f"{MEDIA_REFERENCIA} dias."
    )


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .metric-card {
            background: linear-gradient(
                135deg,
                #111827,
                #1f2937
            );

            padding: 18px 20px;

            border-radius: 14px;

            border: 1px solid #374151;
        }

        .metric-title {
            color: #9ca3af;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .metric-value {
            color: white;
            font-size: 28px;
            font-weight: 700;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.title("🚗 FleetSense")

st.subheader(
    "Dashboard de análise de locações"
)

st.caption(
    "Acompanhe o comportamento das locações "
    "e o teste estatístico da duração média "
    "em relação à referência de 7 dias."
)


st.divider()


# ============================================================
# KPI CARDS
# ============================================================

f_n = len(df_filtrado)

f_media = (
    df_filtrado["dias_locacao"].mean()
)

f_mediana = (
    df_filtrado["dias_locacao"].median()
)

f_desvio = (
    df_filtrado["dias_locacao"].std()
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📋 Contratos",
        f"{f_n:,}".replace(",", "."),
    )


with col2:

    st.metric(
        "📊 Média",
        f"{f_media:.2f} dias",
    )


with col3:

    st.metric(
        "📌 Mediana",
        f"{f_mediana:.2f} dias",
    )


with col4:

    st.metric(
        "📐 Desvio padrão",
        f"{f_desvio:.2f} dias",
    )


# ============================================================
# GRÁFICOS PRINCIPAIS
# ============================================================

st.markdown(
    "### 📈 Visão geral"
)


graf1, graf2 = st.columns(2)


# ============================================================
# DISTRIBUIÇÃO
# ============================================================

with graf1:

    st.markdown(
        "#### Distribuição da duração"
    )

    hist = (
        df_filtrado[
            "dias_locacao"
        ]
        .value_counts()
        .sort_index()
        .rename_axis("Dias")
        .to_frame("Contratos")
    )

    st.bar_chart(
        hist,
        width="stretch",
    )


# ============================================================
# CATEGORIA
# ============================================================

with graf2:

    st.markdown(
        "#### Média por categoria"
    )

    media_categoria = (
        df_filtrado
        .groupby("categoria")[
            "dias_locacao"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .round(2)
    )

    st.bar_chart(
        media_categoria,
        width="stretch",
    )


# ============================================================
# MODELOS
# ============================================================

st.markdown(
    "### 🚘 Desempenho por modelo"
)


# Se id_locacao não existir no CSV,
# criamos um identificador automaticamente.

if "id_locacao" not in df_filtrado.columns:

    df_filtrado["id_locacao"] = range(
        1,
        len(df_filtrado) + 1,
    )


resumo_modelos = (
    df_filtrado
    .groupby(
        [
            "modelo",
            "categoria",
        ]
    )
    .agg(
        contratos=(
            "id_locacao",
            "count",
        ),

        media_dias=(
            "dias_locacao",
            "mean",
        ),

        mediana=(
            "dias_locacao",
            "median",
        ),

        desvio_padrao=(
            "dias_locacao",
            "std",
        ),
    )
    .reset_index()
)


resumo_modelos[
    "media_dias"
] = (
    resumo_modelos[
        "media_dias"
    ].round(2)
)


resumo_modelos[
    "mediana"
] = (
    resumo_modelos[
        "mediana"
    ].round(2)
)


resumo_modelos[
    "desvio_padrao"
] = (
    resumo_modelos[
        "desvio_padrao"
    ].round(2)
)


st.dataframe(
    resumo_modelos,
    width="stretch",
    hide_index=True,
)


# ============================================================
# TESTE DE HIPÓTESE
# ============================================================

st.markdown(
    "### 🧪 Teste de hipótese"
)


teste_col1, teste_col2 = st.columns(
    [1, 1]
)


with teste_col1:

    st.markdown(
        f"""
        **Hipóteses**

        - **H₀:** μ = {MEDIA_REFERENCIA} dias
        - **H₁:** μ ≠ {MEDIA_REFERENCIA} dias
        - **α:** {ALPHA}

        **Resultado da amostra completa**

        - Estatística **t:** `{t_stat:.4f}`
        - **p-valor:** `{p_value:.6f}`
        - **IC 95%:** `{ic_inferior:.2f}` a `{ic_superior:.2f}` dias
        """
    )


with teste_col2:

    if p_value < ALPHA:

        st.error(
            f"**{decisao}**"
        )

    else:

        st.success(
            f"**{decisao}**"
        )


    st.info(
        conclusao
    )


# ============================================================
# COMPARAÇÃO COM REFERÊNCIA
# ============================================================

st.markdown(
    "### 🎯 Média observada × referência"
)


comparacao = pd.DataFrame(
    {
        "Métrica": [
            "Média observada",
            "Média de referência",
        ],

        "Dias": [
            media,
            MEDIA_REFERENCIA,
        ],
    }
).set_index(
    "Métrica"
)


st.bar_chart(
    comparacao,
    width="stretch",
)


# ============================================================
# DADOS
# ============================================================

with st.expander(
    "📋 Visualizar dados"
):

    st.dataframe(
        df_filtrado.sort_values(
            "id_locacao"
        ),
        width="stretch",
        hide_index=True,
    )


    csv = (
        df_filtrado
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        "⬇️ Baixar dados filtrados",

        data=csv,

        file_name="locacoes_filtradas.csv",

        mime="text/csv",
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "FleetSense • Análise estatística de locações • "
    "Teste t de uma amostra"
)
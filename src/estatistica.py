from scipy.stats import ttest_1samp, t
import numpy as np


def teste_media(dados, media_referencia, alpha=0.05):

    n = len(dados)
    media = np.mean(dados)
    desvio_padrao = np.std(dados, ddof=1)

    resultado = ttest_1samp(dados, media_referencia)

    t_statistic = resultado.statistic
    p_value = resultado.pvalue

    if p_value < alpha:
        decisao = "Rejeitar H0"
    else:
        decisao = "Não rejeitar H0"

    erro_padrao = desvio_padrao / np.sqrt(n)

    margem = t.ppf(
        1 - alpha / 2,
        df=n - 1
    ) * erro_padrao

    ic_inferior = media - margem
    ic_superior = media + margem

    if p_value < alpha:
        conclusao = (
            f"A duração média observada ({media:.2f} dias) "
            f"é estatisticamente diferente da média de referência "
            f"de {media_referencia:.2f} dias."
        )
    else:
        conclusao = (
            f"Não há evidências estatísticas suficientes para afirmar "
            f"que a duração média observada ({media:.2f} dias) "
            f"seja diferente da média de referência "
            f"de {media_referencia:.2f} dias."
        )

    return {
        "media": media,
        "t_statistic": t_statistic,
        "p_value": p_value,
        "alpha": alpha,
        "decisao": decisao,
        "ic_inferior": ic_inferior,
        "ic_superior": ic_superior,
        "conclusao": conclusao
    }
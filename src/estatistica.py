from spicy.stats import ttest_1samp

def teste_media(dados, media_referencia):
    """
    Realiza um teste t de uma amostra para verificar se a média dos dados é significativamente 
    diferente da média de referência.
    """
    
    resultado = ttest_1samp(dados, media_referencia)

    return {
        "t_statistic": resultado.statistic,
        "p_value": resultado.pvalue
    }
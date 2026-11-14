
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats

# Configuração da página
st.set_page_config(
    page_title="ENEM 2025 — Inferência Estatística",
    page_icon="📈",
    layout="wide"
)

st.title("ENEM 2025 — Inferência Estatística")

st.write(
    "Intervalos de confiança e testes de hipóteses "
    "utilizando uma amostra aleatória simples "
    "de 1.067 participantes do ENEM 2025."
)

# Localização do arquivo da amostra
PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO = (
    PROJETO
    / "dados_tratados"
    / "amostra_enem_2025.csv"
)

# Carregamento dos dados
@st.cache_data
def carregar_amostra():
    return pd.read_csv(
        ARQUIVO,
        sep=";",
        encoding="utf-8",
        decimal=","
    )

amostra = carregar_amostra()

# Indicadores principais
st.divider()
st.subheader("Informações da amostra")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Participantes",
    f"{len(amostra):,}".replace(",", ".")
)

col2.metric(
    "Média Matemática",
    f"{amostra['NU_NOTA_MT'].mean():.2f}"
)

col3.metric(
    "Média Redação",
    f"{amostra['NU_NOTA_REDACAO'].mean():.2f}"
)


# Intervalo de confiança para a média de Matemática
st.divider()
st.subheader(
    "Intervalo de confiança para a média de Matemática"
)

# Dados amostrais
notas_mt = amostra["NU_NOTA_MT"].dropna()

n = len(notas_mt)
media = notas_mt.mean()
desvio = notas_mt.std(ddof=1)

# Nível de confiança
confianca = st.slider(
    "Selecione o nível de confiança:",
    min_value=90,
    max_value=99,
    value=95,
    step=1
)

alpha = 1 - confianca / 100

# Distribuição t de Student
erro_padrao = desvio / np.sqrt(n)

t_critico = stats.t.ppf(
    1 - alpha / 2,
    df=n - 1
)

margem_erro = t_critico * erro_padrao

limite_inferior = media - margem_erro
limite_superior = media + margem_erro

# Resultados
col1, col2, col3 = st.columns(3)

col1.metric(
    "Média amostral",
    f"{media:.2f}"
)

col2.metric(
    "Margem de erro (pontos)",
    f"{margem_erro:.2f}"
)

col3.metric(
    "Nível de confiança",
    f"{confianca}%"
)

st.success(
    f"Intervalo de confiança de {confianca}%: "
    f"[{limite_inferior:.2f} ; "
    f"{limite_superior:.2f}] pontos"
)

st.caption(
    "Método: intervalo t de Student para a média, "
    "com desvio-padrão estimado pela amostra."
)


# Intervalo de confiança para a média de Redação
st.divider()
st.subheader(
    "Intervalo de confiança para a média de Redação"
)

notas_red = amostra["NU_NOTA_REDACAO"].dropna()

n_red = len(notas_red)
media_red = notas_red.mean()
desvio_red = notas_red.std(ddof=1)

# Utilizar o nível de confiança selecionado anteriormente
erro_padrao_red = desvio_red / np.sqrt(n_red)

t_critico_red = stats.t.ppf(
    1 - alpha / 2,
    df=n_red - 1
)

margem_erro_red = t_critico_red * erro_padrao_red

limite_inferior_red = media_red - margem_erro_red
limite_superior_red = media_red + margem_erro_red

col1, col2, col3 = st.columns(3)

col1.metric(
    "Média amostral — Redação",
    f"{media_red:.2f}"
)

col2.metric(
    "Margem de erro (pontos)",
    f"{margem_erro_red:.2f}"
)

col3.metric(
    "Nível de confiança",
    f"{confianca}%"
)

st.success(
    f"Intervalo de confiança de {confianca}%: "
    f"[{limite_inferior_red:.2f} ; "
    f"{limite_superior_red:.2f}] pontos"
)

st.caption(
    "Método: intervalo t de Student para a média "
    "de Redação, com desvio-padrão amostral."
)


# Teste de hipóteses para duas médias
st.divider()
st.subheader(
    "Teste de hipóteses — Médias de Matemática"
)

st.write(
    "Comparação entre participantes que realizaram "
    "a prova no Rio Grande do Sul (RS) e em "
    "São Paulo (SP)."
)

notas_rs = amostra.loc[
    amostra["SG_UF_PROVA"] == "RS",
    "NU_NOTA_MT"
].dropna()

notas_sp = amostra.loc[
    amostra["SG_UF_PROVA"] == "SP",
    "NU_NOTA_MT"
].dropna()

col1, col2 = st.columns(2)

col1.metric("Participantes RS", len(notas_rs))
col2.metric("Participantes SP", len(notas_sp))

st.write(
    f"Média RS: **{notas_rs.mean():.2f}** pontos"
)

st.write(
    f"Média SP: **{notas_sp.mean():.2f}** pontos"
)

if len(notas_rs) >= 2 and len(notas_sp) >= 2:
    estatistica_t, valor_p = stats.ttest_ind(
        notas_rs,
        notas_sp,
        equal_var=False
    )

    st.write(f"Estatística t: **{estatistica_t:.4f}**")
    st.write(f"Valor-p: **{valor_p:.4f}**")

    if valor_p < 0.05:
        st.success(
            "Resultado: rejeitamos H0 ao nível "
            "de significância de 5%. Há evidência "
            "de diferença entre as médias."
        )
    else:
        st.info(
            "Resultado: não rejeitamos H0 ao nível "
            "de significância de 5%. Não há evidência "
            "estatística suficiente de diferença "
            "entre as médias."
        )
else:
    st.warning(
        "A amostra não possui observações suficientes "
        "para realizar o teste."
    )


# Teste de hipóteses para duas proporções
st.divider()
st.subheader(
    "Teste de hipóteses — Duas proporções"
)

st.write(
    "Comparação da proporção de participantes "
    "com nota de Redação igual ou superior "
    "a 600 pontos no RS e em SP."
)

red_rs = amostra.loc[
    amostra["SG_UF_PROVA"] == "RS",
    "NU_NOTA_REDACAO"
].dropna()

red_sp = amostra.loc[
    amostra["SG_UF_PROVA"] == "SP",
    "NU_NOTA_REDACAO"
].dropna()

n_rs = len(red_rs)
n_sp = len(red_sp)

sucessos_rs = int((red_rs >= 600).sum())
sucessos_sp = int((red_sp >= 600).sum())

prop_rs = sucessos_rs / n_rs
prop_sp = sucessos_sp / n_sp

col1, col2 = st.columns(2)

col1.metric(
    "Proporção RS",
    f"{prop_rs * 100:.2f}%"
)

col2.metric(
    "Proporção SP",
    f"{prop_sp * 100:.2f}%"
)

st.write(
    f"RS: {sucessos_rs} de {n_rs} participantes"
)

st.write(
    f"SP: {sucessos_sp} de {n_sp} participantes"
)

# Teste z para duas proporções
prop_combinada = (
    (sucessos_rs + sucessos_sp)
    / (n_rs + n_sp)
)

erro_padrao = np.sqrt(
    prop_combinada
    * (1 - prop_combinada)
    * (1 / n_rs + 1 / n_sp)
)

if erro_padrao > 0:
    z = (prop_rs - prop_sp) / erro_padrao

    valor_p_prop = 2 * stats.norm.sf(abs(z))

    st.write(f"Estatística z: **{z:.4f}**")
    st.write(f"Valor-p: **{valor_p_prop:.4f}**")

    if valor_p_prop < 0.05:
        st.success(
            "Rejeitamos H0 ao nível de 5%. "
            "Há evidência de diferença entre "
            "as proporções."
        )
    else:
        st.info(
            "Não rejeitamos H0 ao nível de 5%. "
            "Não há evidência estatística "
            "suficiente de diferença entre "
            "as proporções."
        )
else:
    st.warning(
        "Não foi possível calcular o teste z."
    )


# Intervalo de confiança para diferença de proporções
st.divider()
st.subheader(
    "Intervalo de confiança — Diferença de proporções"
)

# Diferença observada entre RS e SP
diferenca_prop = prop_rs - prop_sp

# Erro-padrão não combinado
erro_padrao_ic = np.sqrt(
    prop_rs * (1 - prop_rs) / n_rs
    + prop_sp * (1 - prop_sp) / n_sp
)

# Nível de confiança de 95%
z_critico_ic = stats.norm.ppf(0.975)

margem_ic = z_critico_ic * erro_padrao_ic

limite_inf_prop = diferenca_prop - margem_ic
limite_sup_prop = diferenca_prop + margem_ic

st.metric(
    "Diferença observada (RS - SP)",
    f"{diferenca_prop * 100:.2f} p.p."
)

st.write(
    "Intervalo de confiança de 95% para "
    "a diferença entre proporções:"
)

st.success(
    f"[{limite_inf_prop * 100:.2f} ; "
    f"{limite_sup_prop * 100:.2f}] "
    "pontos percentuais"
)

if limite_inf_prop <= 0 <= limite_sup_prop:
    st.info(
        "O intervalo contém zero. "
        "Isso é compatível com a ausência de "
        "diferença estatisticamente significativa "
        "ao nível de 5%."
    )
else:
    st.success(
        "O intervalo não contém zero, indicando "
        "diferença estatisticamente significativa "
        "ao nível de 5%."
    )

st.caption(
    "Método: intervalo de Wald para diferença "
    "de duas proporções independentes, "
    "com erro-padrão não combinado."
)


# Intervalo de confiança para diferença de médias
st.divider()
st.subheader(
    "Intervalo de confiança — Diferença de médias"
)

# Estatísticas dos dois grupos
media_rs = notas_rs.mean()
media_sp = notas_sp.mean()

var_rs = notas_rs.var(ddof=1)
var_sp = notas_sp.var(ddof=1)

n1 = len(notas_rs)
n2 = len(notas_sp)

# Diferença entre médias
diferenca_medias = media_rs - media_sp

# Erro-padrão de Welch
a = var_rs / n1
b = var_sp / n2

erro_padrao_welch = np.sqrt(a + b)

# Graus de liberdade aproximados
gl_welch = (a + b) ** 2 / (
    (a ** 2) / (n1 - 1)
    + (b ** 2) / (n2 - 1)
)

# Intervalo de confiança de 95%
t_critico_welch = stats.t.ppf(
    0.975,
    df=gl_welch
)

margem_welch = (
    t_critico_welch * erro_padrao_welch
)

limite_inf_medias = (
    diferenca_medias - margem_welch
)

limite_sup_medias = (
    diferenca_medias + margem_welch
)

st.metric(
    "Diferença observada (RS - SP)",
    f"{diferenca_medias:.2f} pontos"
)

st.success(
    f"Intervalo de confiança de 95%: "
    f"[{limite_inf_medias:.2f} ; "
    f"{limite_sup_medias:.2f}] pontos"
)

if limite_inf_medias <= 0 <= limite_sup_medias:
    st.info(
        "O intervalo contém zero. "
        "Não há evidência estatística suficiente "
        "de diferença entre as médias ao nível de 5%."
    )
else:
    st.success(
        "O intervalo não contém zero. "
        "Há evidência estatística de diferença "
        "entre as médias ao nível de 5%."
    )

st.caption(
    "Método: intervalo t de Welch para diferença "
    "entre duas médias independentes, sem pressupor "
    "igualdade das variâncias."
)


# Verificação de integridade da amostra
st.divider()
st.subheader("Verificação da integridade dos dados")

total_registros = len(amostra)

ausentes_mt = amostra["NU_NOTA_MT"].isna().sum()
ausentes_red = amostra["NU_NOTA_REDACAO"].isna().sum()

duplicados = amostra["NU_SEQUENCIAL"].duplicated().sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de registros", total_registros)
col2.metric("Notas MT ausentes", ausentes_mt)
col3.metric("Notas Redação ausentes", ausentes_red)
col4.metric("Identificadores duplicados", duplicados)

if (
    total_registros == 1067
    and ausentes_mt == 0
    and ausentes_red == 0
    and duplicados == 0
):
    st.success(
        "A amostra passou nas verificações "
        "básicas de integridade."
    )
else:
    st.warning(
        "Foram identificadas inconsistências "
        "que precisam ser verificadas."
    )


# Informações metodológicas
st.divider()
st.subheader("Metodologia estatística")

st.markdown("""
**População:** 3.244.348 participantes do ENEM 2025
com notas válidas de Matemática e Redação.

**Amostra:** 1.067 participantes selecionados por
amostragem aleatória simples, sem reposição.

**Método de dimensionamento:** nível de confiança de
95%, margem de erro de 3 pontos percentuais,
proporção esperada de 50% e correção para
população finita.

**Intervalos de confiança para médias:**
distribuição t de Student, com desvio-padrão
estimado pela amostra.

**Comparação de médias:** teste t de Welch,
bilateral, para grupos independentes.

**Comparação de proporções:** teste z bilateral
para duas proporções independentes.

**Intervalo para diferença de médias:**
método de Welch.

**Intervalo para diferença de proporções:**
método de Wald, com erro-padrão não combinado.

**Nível de significância dos testes:** 5%.
""")

st.info(
    "A margem de erro de 3 pontos percentuais "
    "utilizada no dimensionamento da amostra "
    "refere-se à estimação de proporções, "
    "não às médias das notas."
)


# Teste de hipótese para uma média populacional
st.divider()
st.subheader(
    "Teste de hipótese — Média populacional de Matemática"
)

st.write(
    "Investigamos se a média populacional "
    "de Matemática é diferente de 500 pontos."
)

st.latex(r"H_0: \mu = 500")
st.latex(r"H_1: \mu \neq 500")

notas_mt = amostra["NU_NOTA_MT"].dropna()

media_hipotetica = 500

t_calculado, p_valor_media = stats.ttest_1samp(
    notas_mt,
    popmean=media_hipotetica
)

st.write(
    f"Média amostral: **{notas_mt.mean():.2f}**"
)

st.write(
    f"Estatística t: **{t_calculado:.4f}**"
)

st.write(
    f"Valor-p: **{p_valor_media:.4f}**"
)

st.write("Nível de significância: **5%**")

if p_valor_media < 0.05:
    st.success(
        "Rejeitamos H0. Há evidência estatística "
        "de que a média populacional de Matemática "
        "é diferente de 500 pontos."
    )
else:
    st.info(
        "Não rejeitamos H0. Não há evidência "
        "estatística suficiente para afirmar "
        "que a média populacional de Matemática "
        "seja diferente de 500 pontos."
    )

# Comparação com o parâmetro populacional conhecido
media_populacional_mt = 520.12

st.write(
    f"Média observada na população: "
    f"**{media_populacional_mt:.2f}** pontos"
)

st.caption(
    "O teste utiliza exclusivamente a amostra. "
    "A média populacional conhecida é apresentada "
    "apenas para comparação e validação da inferência."
)


# Teste de hipótese para média de Redação
st.divider()
st.subheader(
    "Teste de hipótese — Média populacional de Redação"
)

st.write(
    "Investigamos se a média populacional "
    "de Redação é diferente de 600 pontos."
)

st.latex(r"H_0: \mu = 600")
st.latex(r"H_1: \mu \neq 600")

notas_redacao = amostra[
    "NU_NOTA_REDACAO"
].dropna()

t_redacao, p_redacao = stats.ttest_1samp(
    notas_redacao,
    popmean=600
)

st.write(
    f"Média amostral: "
    f"**{notas_redacao.mean():.2f}**"
)

st.write(
    f"Estatística t: **{t_redacao:.4f}**"
)

st.write(
    f"Valor-p: **{p_redacao:.4f}**"
)

st.write("Nível de significância: **5%**")

if p_redacao < 0.05:
    st.success(
        "Rejeitamos H0. Há evidência estatística "
        "de que a média populacional de Redação "
        "é diferente de 600 pontos."
    )
else:
    st.info(
        "Não rejeitamos H0. Não há evidência "
        "estatística suficiente para afirmar "
        "que a média populacional de Redação "
        "seja diferente de 600 pontos."
    )

st.write(
    "Média observada na população: "
    "**590.08** pontos"
)

st.caption(
    "O teste utiliza exclusivamente a amostra. "
    "A média populacional conhecida é apresentada "
    "apenas para comparação."
)


# Inferência para uma proporção populacional
st.divider()
st.subheader(
    "Inferência — Proporção com Redação >= 600"
)

st.write(
    "Investigamos se a proporção populacional "
    "de participantes com nota de Redação "
    "igual ou superior a 600 é diferente de 50%."
)

st.latex(r"H_0: p = 0.50")
st.latex(r"H_1: p \neq 0.50")

# Dados da amostra
notas = amostra["NU_NOTA_REDACAO"].dropna()

n_prop = len(notas)
sucessos = int((notas >= 600).sum())

p_amostral = sucessos / n_prop
p_hipotetica = 0.50

# Teste z para uma proporção
erro_padrao_h0 = np.sqrt(
    p_hipotetica * (1 - p_hipotetica) / n_prop
)

z_prop = (
    (p_amostral - p_hipotetica)
    / erro_padrao_h0
)

p_valor = 2 * stats.norm.sf(abs(z_prop))

st.write(f"Participantes analisados: **{n_prop}**")
st.write(f"Notas >= 600: **{sucessos}**")

st.write(
    f"Proporção amostral: **{p_amostral * 100:.2f}%**"
)

st.write(f"Estatística z: **{z_prop:.4f}**")
st.write(f"Valor-p: **{p_valor:.4f}**")
st.write("Nível de significância: **5%**")

if p_valor < 0.05:
    st.success(
        "Rejeitamos H0. Há evidência estatística "
        "de que a proporção populacional "
        "é diferente de 50%."
    )
else:
    st.info(
        "Não rejeitamos H0. Não há evidência "
        "estatística suficiente de que a "
        "proporção populacional difira de 50%."
    )

# Intervalo de confiança de Wilson (95%)
z_critico = stats.norm.ppf(0.975)

denominador = 1 + z_critico**2 / n_prop

centro = (
    p_amostral + z_critico**2 / (2 * n_prop)
) / denominador

margem = (
    z_critico / denominador
    * np.sqrt(
        p_amostral * (1 - p_amostral) / n_prop
        + z_critico**2 / (4 * n_prop**2)
    )
)

limite_inferior = centro - margem
limite_superior = centro + margem

st.write("Intervalo de confiança de 95% (Wilson):")

st.success(
    f"[{limite_inferior * 100:.2f}% ; "
    f"{limite_superior * 100:.2f}%]"
)


# Comparação com a proporção populacional real
st.markdown(
    "#### Comparação com a população"
)

ARQUIVO_POPULACAO = (
    PROJETO
    / "dados_tratados"
    / "populacao_enem_2025.parquet"
)


@st.cache_data
def calcular_proporcao_populacional_600():
    notas = pd.read_parquet(
        ARQUIVO_POPULACAO,
        columns=["NU_NOTA_REDACAO"]
    )["NU_NOTA_REDACAO"].dropna()

    return (notas >= 600).mean()

p_populacional = (
    calcular_proporcao_populacional_600()
)

col1, col2 = st.columns(2)

col1.metric(
    "Proporção populacional",
    f"{p_populacional * 100:.2f}%"
)

col2.metric(
    "Proporção amostral",
    f"{p_amostral * 100:.2f}%"
)

diferenca = (
    p_amostral - p_populacional
) * 100

st.write(
    f"Diferença (amostra - população): "
    f"**{diferenca:+.2f} pontos percentuais**"
)

if limite_inferior <= p_populacional <= limite_superior:
    st.success(
        "A proporção populacional real está "
        "contida no intervalo de confiança "
        "estimado a partir da amostra."
    )
else:
    st.warning(
        "A proporção populacional real não está "
        "contida no intervalo de confiança "
        "estimado a partir da amostra."
    )


# Segundo teste para uma proporção populacional
st.divider()
st.subheader(
    "Inferência — Proporção com Redação >= 800"
)

st.write(
    "Investigamos se a proporção populacional "
    "de participantes com nota de Redação "
    "igual ou superior a 800 difere de 20%."
)

st.latex(r"H_0: p = 0.20")
st.latex(r"H_1: p \neq 0.20")

# Dados da amostra
notas_800 = amostra[
    "NU_NOTA_REDACAO"
].dropna()

n_800 = len(notas_800)
sucessos_800 = int((notas_800 >= 800).sum())

p_amostral_800 = sucessos_800 / n_800
p_hipotetica_800 = 0.20

# Teste z para uma proporção
erro_padrao_h0_800 = np.sqrt(
    p_hipotetica_800
    * (1 - p_hipotetica_800)
    / n_800
)

z_800 = (
    p_amostral_800 - p_hipotetica_800
) / erro_padrao_h0_800

p_valor_800 = 2 * stats.norm.sf(abs(z_800))

st.write(
    f"Participantes com nota >= 800: "
    f"**{sucessos_800} de {n_800}**"
)

st.write(
    f"Proporção amostral: "
    f"**{p_amostral_800 * 100:.2f}%**"
)

st.write(f"Estatística z: **{z_800:.4f}**")
st.write(f"Valor-p: **{p_valor_800:.4f}**")
st.write("Nível de significância: **5%**")

if p_valor_800 < 0.05:
    st.success(
        "Rejeitamos H0. Há evidência estatística "
        "de que a proporção populacional "
        "difere de 20%."
    )
else:
    st.info(
        "Não rejeitamos H0. Não há evidência "
        "estatística suficiente de que a "
        "proporção populacional difira de 20%."
    )

# Intervalo de confiança de Wilson (95%)
z_critico_800 = stats.norm.ppf(0.975)

denominador_800 = 1 + z_critico_800**2 / n_800

centro_800 = (
    p_amostral_800
    + z_critico_800**2 / (2 * n_800)
) / denominador_800

margem_800 = (
    z_critico_800 / denominador_800
    * np.sqrt(
        p_amostral_800
        * (1 - p_amostral_800) / n_800
        + z_critico_800**2 / (4 * n_800**2)
    )
)

limite_inf_800 = centro_800 - margem_800
limite_sup_800 = centro_800 + margem_800

st.write(
    "Intervalo de confiança de 95% (Wilson):"
)

st.success(
    f"[{limite_inf_800 * 100:.2f}% ; "
    f"{limite_sup_800 * 100:.2f}%]"
)


# Comparação com a proporção populacional: Redação >= 800
st.markdown(
    "#### Comparação com a população — Redação >= 800"
)


@st.cache_data
def calcular_proporcao_populacional_800():
    notas = pd.read_parquet(
        ARQUIVO_POPULACAO,
        columns=["NU_NOTA_REDACAO"]
    )["NU_NOTA_REDACAO"].dropna()

    return (notas >= 800).mean()

p_populacional_800 = (
    calcular_proporcao_populacional_800()
)

col1, col2 = st.columns(2)

col1.metric(
    "Proporção populacional",
    f"{p_populacional_800 * 100:.2f}%"
)

col2.metric(
    "Proporção amostral",
    f"{p_amostral_800 * 100:.2f}%"
)

diferenca_800 = (
    p_amostral_800 - p_populacional_800
) * 100

st.write(
    f"Diferença (amostra - população): "
    f"**{diferenca_800:+.2f} pontos percentuais**"
)

if limite_inf_800 <= p_populacional_800 <= limite_sup_800:
    st.success(
        "A proporção populacional está contida "
        "no intervalo de confiança de 95%."
    )
else:
    st.warning(
        "A proporção populacional não está contida "
        "no intervalo de confiança de 95%."
    )


# Quadro-resumo da inferência estatística
st.divider()
st.subheader(
    "Síntese — População versus amostra"
)

resumo = pd.DataFrame({
    "Parâmetro": [
        "Média Matemática",
        "Média Redação",
        "Proporção Redação >= 600",
        "Proporção Redação >= 800"
    ],
    "População": [
        "520,12",
        "590,08",
        f"{p_populacional * 100:.2f}%",
        f"{p_populacional_800 * 100:.2f}%"
    ],
    "Amostra": [
        f"{amostra['NU_NOTA_MT'].mean():.2f}",
        f"{amostra['NU_NOTA_REDACAO'].mean():.2f}",
        f"{p_amostral * 100:.2f}%",
        f"{p_amostral_800 * 100:.2f}%"
    ],
    "IC de 95%": [
        f"[{stats.t.interval(0.95, len(amostra)-1, loc=amostra['NU_NOTA_MT'].mean(), scale=stats.sem(amostra['NU_NOTA_MT']))[0]:.2f} ; {stats.t.interval(0.95, len(amostra)-1, loc=amostra['NU_NOTA_MT'].mean(), scale=stats.sem(amostra['NU_NOTA_MT']))[1]:.2f}]",
        f"[{stats.t.interval(0.95, len(amostra)-1, loc=amostra['NU_NOTA_REDACAO'].mean(), scale=stats.sem(amostra['NU_NOTA_REDACAO']))[0]:.2f} ; {stats.t.interval(0.95, len(amostra)-1, loc=amostra['NU_NOTA_REDACAO'].mean(), scale=stats.sem(amostra['NU_NOTA_REDACAO']))[1]:.2f}]",
        f"[{limite_inferior * 100:.2f}% ; "
        f"{limite_superior * 100:.2f}%]",
        f"[{limite_inf_800 * 100:.2f}% ; "
        f"{limite_sup_800 * 100:.2f}%]"
    ]
})

st.dataframe(
    resumo,
    hide_index=True,
    width="stretch"
)

st.caption(
    "As médias e proporções populacionais são "
    "calculadas diretamente da população. "
    "As estimativas e os intervalos de confiança "
    "utilizam exclusivamente a amostra."
)

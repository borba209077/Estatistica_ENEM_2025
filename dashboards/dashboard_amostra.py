

from pathlib import Path

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="ENEM 2025 - População",
    page_icon="📊",
    layout="wide"
)

# Localização do arquivo de dados
PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO = (
    PROJETO
    / "dados_tratados"
    / "amostra_enem_2025.csv"
)


# Leitura dos dados


@st.cache_data(show_spinner="Carregando dados do ENEM...")
def carregar_dados():
    return pd.read_csv(
        ARQUIVO,
        sep=";",
        encoding="utf-8",
        decimal=",",
        usecols=[
            "NU_NOTA_MT",
            "NU_NOTA_REDACAO",
            "SG_UF_PROVA",
            "TP_STATUS_REDACAO"
        ],
        dtype={
            "NU_NOTA_MT": "float32",
            "NU_NOTA_REDACAO": "float32",
            "SG_UF_PROVA": "category",
            "TP_STATUS_REDACAO": "category"
        }
    )

dados = carregar_dados()

# Estatísticas descritivas
estatisticas = dados[
    ["NU_NOTA_MT", "NU_NOTA_REDACAO"]
].agg(["mean", "median", "std"])

# Título
st.title("ENEM 2025 — Estatística Descritiva da Amostra")

st.write(
    "Análise descritiva da amostra aleatória simples "
    "de 1.067 participantes do ENEM 2025."
)

st.divider()

# Indicadores
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Participantes",
        f"{len(dados):,}".replace(",", ".")
    )

with col2:
    st.metric(
        "Média Matemática",
        f"{estatisticas.loc['mean', 'NU_NOTA_MT']:.2f}"
    )

with col3:
    st.metric(
        "Média Redação",
        f"{estatisticas.loc['mean', 'NU_NOTA_REDACAO']:.2f}"
    )

st.divider()


st.divider()
st.subheader("Distribuição das notas por UF")

# Filtro de unidade da Federação
ufs_hist = sorted(
    dados["SG_UF_PROVA"].dropna().unique().tolist()
)

uf_hist = st.selectbox(
    "Selecione a UF para visualizar os histogramas:",
    options=["Brasil"] + ufs_hist,
    key="filtro_histogramas"
)

# Aplicar o filtro
if uf_hist == "Brasil":
    dados_filtrados = dados
else:
    dados_filtrados = dados.loc[
        dados["SG_UF_PROVA"] == uf_hist
    ]

st.caption(
    f"Participantes considerados nos gráficos: "
    f"{len(dados_filtrados):,}".replace(",", ".")
)

# Intervalos de 25 pontos
limites = np.arange(0, 1025, 25)

# Dois gráficos lado a lado
col_graf1, col_graf2 = st.columns(2)

graficos = [
    ("NU_NOTA_MT", "Matemática", col_graf1),
    ("NU_NOTA_REDACAO", "Redação", col_graf2)
]

for coluna, titulo, coluna_tela in graficos:

    frequencias, bordas = np.histogram(
        dados_filtrados[coluna].dropna(),
        bins=limites
    )

    grafico_dados = pd.DataFrame({
        "Intervalo": [
            f"{int(bordas[i])} a {int(bordas[i+1])}"
            for i in range(len(frequencias))
        ],
        "Participantes": frequencias
    })

    fig = px.bar(
        grafico_dados,
        x="Intervalo",
        y="Participantes",
        title=f"Notas de {titulo} — {uf_hist}",
        labels={
            "Intervalo": "Faixa de notas",
            "Participantes": "Participantes"
        }
    )

    fig.update_layout(
        height=420,
        xaxis_tickangle=-45,
        margin=dict(l=20, r=20, t=60, b=90)
    )

    # Exibir o gráfico na coluna correspondente
    with coluna_tela:
        st.plotly_chart(
            fig,
            use_container_width=True
        )



st.divider()
st.subheader("Análise por unidade da Federação")

# Estatísticas por estado
estatisticas_uf = (
    dados.groupby(
        "SG_UF_PROVA",
        observed=True
    )
    .agg(
        Participantes=("NU_NOTA_MT", "size"),
        Media_Matematica=("NU_NOTA_MT", "mean"),
        Media_Redacao=("NU_NOTA_REDACAO", "mean")
    )
    .reset_index()
)

# Seleção interativa do estado
ufs = sorted(
    estatisticas_uf["SG_UF_PROVA"].astype(str).tolist()
)

uf_selecionada = st.selectbox(
    "Selecione uma unidade da Federação:",
    options=["Todas"] + ufs
)

if uf_selecionada != "Todas":
    resultado = estatisticas_uf[
        estatisticas_uf["SG_UF_PROVA"].astype(str)
        == uf_selecionada
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Participantes",
        f"{int(resultado['Participantes']):,}".replace(",", ".")
    )

    col2.metric(
        "Média Matemática",
        f"{resultado['Media_Matematica']:.2f}"
    )

    col3.metric(
        "Média Redação",
        f"{resultado['Media_Redacao']:.2f}"
    )

# Comparação entre estados
tabela_uf = estatisticas_uf.rename(columns={
    "SG_UF_PROVA": "UF",
    "Media_Matematica": "Matemática",
    "Media_Redacao": "Redação"
})

st.dataframe(
    tabela_uf.style.format({
        "Participantes": "{:,.0f}",
        "Matemática": "{:.2f}",
        "Redação": "{:.2f}"
    }),
    hide_index=True,
    use_container_width=True
)

# Gráfico comparativo das médias
grafico_uf = tabela_uf.melt(
    id_vars="UF",
    value_vars=["Matemática", "Redação"],
    var_name="Prova",
    value_name="Nota média"
)

fig_uf = px.bar(
    grafico_uf,
    x="UF",
    y="Nota média",
    color="Prova",
    barmode="group",
    title="Médias de Matemática e Redação por UF"
)

fig_uf.update_layout(
    height=500,
    xaxis_title="Unidade da Federação",
    yaxis_title="Nota média"
)

st.plotly_chart(
    fig_uf,
    use_container_width=True
)


st.divider()
st.subheader("Medidas de posição e dispersão")

# Utilizar a mesma UF selecionada nos histogramas
dados_estatisticas = dados_filtrados

colunas_notas = {
    "Matemática": "NU_NOTA_MT",
    "Redação": "NU_NOTA_REDACAO"
}

resultados = []

for prova, coluna in colunas_notas.items():
    notas = dados_estatisticas[coluna].dropna()

    q1 = notas.quantile(0.25)
    q3 = notas.quantile(0.75)

    resultados.append({
        "Prova": prova,
        "Participantes": len(notas),
        "Média": notas.mean(),
        "Mediana": notas.median(),
        "Desvio-padrão": notas.std(ddof=0),
        "Mínimo": notas.min(),
        "Q1": q1,
        "Q3": q3,
        "Máximo": notas.max(),
        "Amplitude interquartil": q3 - q1
    })

tabela_medidas = pd.DataFrame(resultados)

st.write(f"Unidade geográfica selecionada: **{uf_hist}**")

st.dataframe(
    tabela_medidas.style.format({
        "Participantes": "{:,.0f}",
        "Média": "{:.2f}",
        "Mediana": "{:.2f}",
        "Desvio-padrão": "{:.2f}",
        "Mínimo": "{:.2f}",
        "Q1": "{:.2f}",
        "Q3": "{:.2f}",
        "Máximo": "{:.2f}",
        "Amplitude interquartil": "{:.2f}"
    }),
    hide_index=True,
    use_container_width=True
)


st.subheader("Boxplots das notas")

# Calcular estatísticas dos boxplots sem enviar
# milhões de observações ao navegador
col_box1, col_box2 = st.columns(2)

for prova, coluna, coluna_tela in [
    ("Matemática", "NU_NOTA_MT", col_box1),
    ("Redação", "NU_NOTA_REDACAO", col_box2)
]:
    notas = dados_estatisticas[coluna].dropna()

    q1 = float(notas.quantile(0.25))
    mediana = float(notas.median())
    q3 = float(notas.quantile(0.75))
    iqr = q3 - q1

    # Limites convencionais para identificação
    # de valores atípicos (regra de 1,5 x IQR)
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    # Extremos dos bigodes dentro dos limites
    valores_bigodes = notas[
        notas.between(limite_inferior, limite_superior)
    ]

    inferior = float(valores_bigodes.min())
    superior = float(valores_bigodes.max())

    import plotly.graph_objects as go

    fig_box = go.Figure()

    fig_box.add_trace(
        go.Box(
            q1=[q1],
            median=[mediana],
            q3=[q3],
            lowerfence=[inferior],
            upperfence=[superior],
            name=prova,
            boxpoints=False
        )
    )

    fig_box.update_layout(
        title=f"{prova} — {uf_hist}",
        yaxis_title="Nota",
        yaxis_range=[0, 1000],
        height=420
    )

    with coluna_tela:
        st.plotly_chart(
            fig_box,
            use_container_width=True
        )

st.caption(
    "Os boxplots apresentam quartis, mediana e "
    "bigodes calculados pela regra de 1,5 × IQR. "
    "Os valores atípicos individuais não são exibidos."
)


st.divider()
st.subheader("Análise qualitativa — Situação da redação")

# Categorias oficiais do dicionário do ENEM
situacoes = {
    "1": "Sem problemas",
    "2": "Anulada",
    "3": "Cópia do texto motivador",
    "4": "Em branco",
    "6": "Fuga ao tema",
    "7": "Não atendimento ao tipo textual",
    "8": "Texto insuficiente",
    "9": "Parte desconectada"
}

# Utilizar o filtro geográfico dos histogramas
frequencias_redacao = (
    dados_filtrados["TP_STATUS_REDACAO"]
    .astype("string")
    .value_counts()
    .rename_axis("Código")
    .reset_index(name="Frequência")
)

frequencias_redacao["Situação"] = (
    frequencias_redacao["Código"]
    .map(situacoes)
    .fillna("Outra situação")
)

total = frequencias_redacao["Frequência"].sum()

frequencias_redacao["Percentual"] = (
    frequencias_redacao["Frequência"] / total * 100
)

st.write(
    f"Distribuição das situações da redação — **{uf_hist}**"
)

st.dataframe(
    frequencias_redacao[
        ["Situação", "Frequência", "Percentual"]
    ].style.format({
        "Frequência": "{:,.0f}",
        "Percentual": "{:.2f}%"
    }),
    hide_index=True,
    use_container_width=True
)

# Gráfico de barras
fig_situacoes = px.bar(
    frequencias_redacao.sort_values("Frequência"),
    x="Frequência",
    y="Situação",
    orientation="h",
    title=f"Situação da redação — {uf_hist}",
    labels={
        "Frequência": "Número de participantes",
        "Situação": "Classificação"
    }
)

fig_situacoes.update_layout(
    height=450,
    yaxis_title=""
)

st.plotly_chart(
    fig_situacoes,
    use_container_width=True
)


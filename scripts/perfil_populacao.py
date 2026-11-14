
from pathlib import Path
import pandas as pd

projeto = Path(__file__).resolve().parent.parent
arquivos = list(
    (projeto / "dados_originais").rglob(
        "RESULTADOS_2025.csv"
    )
)

if len(arquivos) != 1:
    raise FileNotFoundError("Arquivo CSV não encontrado.")

colunas = [
    "NU_NOTA_MT",
    "NU_NOTA_REDACAO",
    "TP_PRESENCA_MT",
    "TP_STATUS_REDACAO",
    "SG_UF_PROVA"
]

total = 0
situacao_redacao = pd.Series(dtype="int64")
presenca_mt = pd.Series(dtype="int64")
ufs = pd.Series(dtype="int64")

for bloco in pd.read_csv(
    arquivos[0],
    sep=";",
    encoding="latin-1",
    usecols=colunas,
    dtype=str,
    chunksize=100_000
):
    mt = pd.to_numeric(
        bloco["NU_NOTA_MT"].str.replace(",", "."),
        errors="coerce"
    )
    red = pd.to_numeric(
        bloco["NU_NOTA_REDACAO"].str.replace(",", "."),
        errors="coerce"
    )

    validos = mt.between(0, 1000) & red.between(0, 1000)
    dados = bloco.loc[validos]

    total += len(dados)

    for coluna, acumulador in [
        ("TP_STATUS_REDACAO", "redacao"),
        ("TP_PRESENCA_MT", "presenca"),
        ("SG_UF_PROVA", "uf")
    ]:
        contagem = dados[coluna].value_counts(dropna=False)

        if acumulador == "redacao":
            situacao_redacao = situacao_redacao.add(
                contagem, fill_value=0
            )
        elif acumulador == "presenca":
            presenca_mt = presenca_mt.add(
                contagem, fill_value=0
            )
        else:
            ufs = ufs.add(contagem, fill_value=0)

print("\nPERFIL DA POPULAÇÃO CANDIDATA")
print("----------------------------")
print(f"Registros: {total:,}")

print("\nSITUAÇÃO DA REDAÇÃO")
print(situacao_redacao.sort_index().astype(int))

print("\nPRESENÇA EM MATEMÁTICA")
print(presenca_mt.sort_index().astype(int))

print("\nDISTRIBUIÇÃO POR UF")
print(ufs.sort_index().astype(int))

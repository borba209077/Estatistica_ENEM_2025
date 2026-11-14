
from pathlib import Path
import pandas as pd

projeto = Path(__file__).resolve().parent.parent
arquivos = list(
    (projeto / "dados_originais").rglob(
        "RESULTADOS_2025.csv"
    )
)

if len(arquivos) != 1:
    raise FileNotFoundError(
        "Arquivo RESULTADOS_2025.csv não localizado."
    )

arquivo = arquivos[0]

variaveis = [
    "NU_SEQUENCIAL",
    "NU_NOTA_MT",
    "NU_NOTA_REDACAO",
    "NU_NOTA_CN",
    "TP_PRESENCA_MT",
    "TP_DEPENDENCIA_ADM_ESC",
    "SG_UF_PROVA",
    "TP_STATUS_REDACAO"
]

total = 0
ausentes = pd.Series(0, index=variaveis, dtype="int64")
presenca = pd.Series(dtype="int64")
identificadores = set()
duplicados = 0

for bloco in pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin-1",
    usecols=variaveis,
    dtype=str,
    chunksize=100_000
):
    total += len(bloco)
    ausentes += bloco.isna().sum()

    contagem = bloco["TP_PRESENCA_MT"].value_counts(
        dropna=False
    )
    presenca = presenca.add(
        contagem, fill_value=0
    ).astype("int64")

    ids = bloco["NU_SEQUENCIAL"]
    duplicados += ids.duplicated().sum()
    novos = set(ids.dropna())
    duplicados += len(novos & identificadores)
    identificadores.update(novos)

print("\nQUALIDADE DOS DADOS")
print("-------------------")
print(f"Total de registros: {total:,}")
print(f"Identificadores duplicados: {duplicados:,}")

print("\nVALORES AUSENTES")
for variavel in variaveis:
    qtd = int(ausentes[variavel])
    percentual = qtd / total * 100
    print(f"{variavel}: {qtd:,} ({percentual:.2f}%)")

print("\nPRESENÇA NA PROVA DE MATEMÁTICA")
print(presenca.sort_index().to_string())

print("\nAnálise de qualidade concluída!")

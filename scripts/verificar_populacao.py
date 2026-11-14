
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
        "RESULTADOS_2025.csv não encontrado."
    )

arquivo = arquivos[0]

total = 0
com_matematica = 0
com_redacao = 0
com_ambas = 0
com_ambas_validas = 0

for bloco in pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin-1",
    usecols=[
        "NU_NOTA_MT",
        "NU_NOTA_REDACAO",
        "TP_PRESENCA_MT",
        "TP_STATUS_REDACAO"
    ],
    chunksize=100_000,
    decimal=","
):
    total += len(bloco)

    mt = pd.to_numeric(
        bloco["NU_NOTA_MT"], errors="coerce"
    )
    red = pd.to_numeric(
        bloco["NU_NOTA_REDACAO"], errors="coerce"
    )

    tem_mt = mt.notna()
    tem_red = red.notna()
    ambas = tem_mt & tem_red

    com_matematica += int(tem_mt.sum())
    com_redacao += int(tem_red.sum())
    com_ambas += int(ambas.sum())

    # Confere se as notas estão no intervalo 0 a 1000
    validas = (
        ambas
        & mt.between(0, 1000)
        & red.between(0, 1000)
    )
    com_ambas_validas += int(validas.sum())

print("\nVERIFICAÇÃO DA POPULAÇÃO")
print("-----------------------")
print(f"Total de registros: {total:,}")
print(f"Com nota de Matemática: {com_matematica:,}")
print(f"Com nota de Redação: {com_redacao:,}")
print(f"Com ambas as notas: {com_ambas:,}")
print(
    "Com ambas as notas no intervalo 0 a 1000:",
    f"{com_ambas_validas:,}"
)

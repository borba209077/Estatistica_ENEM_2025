
from pathlib import Path
import pandas as pd

projeto = Path(__file__).resolve().parent.parent

arquivo = (
    projeto / "dados_tratados"
    / "amostra_enem_2025.csv"
)

amostra = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8",
    decimal=",",
    dtype={"NU_SEQUENCIAL": str}
)

print("\nVALIDAÇÃO FINAL DA AMOSTRA")
print("-------------------------")

print("Número de registros:", len(amostra))
print("Número de variáveis:", len(amostra.columns))

print(
    "Identificadores duplicados:",
    amostra["NU_SEQUENCIAL"].duplicated().sum()
)

for coluna in ["NU_NOTA_MT", "NU_NOTA_REDACAO"]:
    notas = pd.to_numeric(
        amostra[coluna], errors="coerce"
    )

    print(f"\n{coluna}")
    print("Notas ausentes:", notas.isna().sum())
    print("Notas fora de 0 a 1000:",
          (~notas.between(0, 1000)).sum())
    print("Mínimo:", notas.min())
    print("Máximo:", notas.max())

assert len(amostra) == 1067
assert amostra["NU_SEQUENCIAL"].is_unique

for coluna in ["NU_NOTA_MT", "NU_NOTA_REDACAO"]:
    assert amostra[coluna].notna().all()
    assert amostra[coluna].between(0, 1000).all()

print("\nAMOSTRA VALIDADA COM SUCESSO!")

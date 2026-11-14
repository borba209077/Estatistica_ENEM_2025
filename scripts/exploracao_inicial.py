
from pathlib import Path
import pandas as pd

# Localizar a pasta principal do projeto
projeto = Path(__file__).resolve().parent.parent

# Localizar o arquivo original
pasta_dados = projeto / "dados_originais"
arquivos = list(pasta_dados.rglob("RESULTADOS_2025.csv"))

if len(arquivos) != 1:
    raise FileNotFoundError(
        "Não foi encontrado exatamente um arquivo "
        "RESULTADOS_2025.csv em dados_originais."
    )

arquivo = arquivos[0]

print("Iniciando análise dos microdados do ENEM 2025...")
print("Arquivo:", arquivo.name)

# Ler somente os nomes das colunas
cabecalho = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin-1",
    nrows=0
)

colunas = cabecalho.columns.tolist()

# Contar registros sem carregar toda a base
total = 0

for bloco in pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin-1",
    chunksize=100_000,
    dtype=str
):
    total += len(bloco)

print("\nRESULTADOS DA EXPLORAÇÃO")
print("------------------------")
print(f"Total de observações: {total:,}")
print(f"Total de variáveis: {len(colunas)}")

print("\nVARIÁVEIS DISPONÍVEIS")
for coluna in colunas:
    print(coluna)

print("\nExploração inicial concluída!")

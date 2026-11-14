
from pathlib import Path
import pandas as pd

# Localizar a pasta principal do projeto
PROJETO = Path(__file__).resolve().parent.parent

arquivo_csv = (
    PROJETO / "dados_tratados" / "populacao_enem_2025.csv"
)

arquivo_parquet = (
    PROJETO / "dados_tratados" / "populacao_enem_2025.parquet"
)

print("Lendo o arquivo CSV da população...")

populacao = pd.read_csv(
    arquivo_csv,
    sep=";",
    encoding="utf-8",
    decimal=","
)

print(f"Registros lidos: {len(populacao):,}")
print(f"Variáveis: {len(populacao.columns)}")

print("Convertendo para Parquet...")

populacao.to_parquet(
    arquivo_parquet,
    engine="pyarrow",
    compression="zstd",
    index=False
)

tamanho_mb = arquivo_parquet.stat().st_size / (1024 ** 2)

print("Conversão concluída!")
print(f"Tamanho do Parquet: {tamanho_mb:.2f} MB")

# Conferir a quantidade de registros no arquivo gerado
import pyarrow.parquet as pq

metadados = pq.ParquetFile(arquivo_parquet).metadata

print(
    f"Registros no Parquet: {metadados.num_rows:,}"
)

if metadados.num_rows == len(populacao):
    print("Validação: quantidade de registros preservada.")
else:
    print("ATENÇÃO: divergência na quantidade de registros!")

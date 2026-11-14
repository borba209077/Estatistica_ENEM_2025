
from pathlib import Path
import numpy as np
import pandas as pd

# Configurações
N = 3_244_348
n = 1_067
SEMENTE = 2025

PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_POPULACAO = (
    PROJETO / "dados_tratados"
    / "populacao_enem_2025.csv"
)

ARQUIVO_AMOSTRA = (
    PROJETO / "dados_tratados"
    / "amostra_enem_2025.csv"
)

if not ARQUIVO_POPULACAO.exists():
    raise FileNotFoundError(
        "Arquivo da população não encontrado."
    )

# Sorteio aleatório simples sem reposição
gerador = np.random.default_rng(SEMENTE)

indices_sorteados = np.sort(
    gerador.choice(N, size=n, replace=False)
)

# Ler a população em blocos
partes_amostra = []
inicio = 0

for bloco in pd.read_csv(
    ARQUIVO_POPULACAO,
    sep=";",
    encoding="utf-8",
    dtype=str,
    chunksize=100_000
):
    fim = inicio + len(bloco)

    # Identificar índices sorteados neste bloco
    posicoes = indices_sorteados[
        (indices_sorteados >= inicio)
        & (indices_sorteados < fim)
    ] - inicio

    if len(posicoes) > 0:
        partes_amostra.append(
            bloco.iloc[posicoes].copy()
        )

    inicio = fim

# Verificar o total de registros da população
if inicio != N:
    raise ValueError(
        f"População esperada: {N}; encontrada: {inicio}"
    )

# Reunir os participantes sorteados
amostra = pd.concat(
    partes_amostra,
    ignore_index=True
)

# Validar o sorteio
assert len(amostra) == n

assert (
    amostra["NU_SEQUENCIAL"].is_unique
)

# Salvar a amostra
amostra.to_csv(
    ARQUIVO_AMOSTRA,
    sep=";",
    index=False,
    encoding="utf-8"
)

print("\nSORTEIO CONCLUÍDO")
print("----------------------------")
print(f"População: {N:,}")
print(f"Amostra: {len(amostra):,}")
print(f"Semente aleatória: {SEMENTE}")

print("\nPrimeiros 10 participantes sorteados:")
print(
    amostra["NU_SEQUENCIAL"]
    .head(10)
    .to_string(index=False)
)

print("\nArquivo gerado:")
print(ARQUIVO_AMOSTRA)

print("\nVALIDAÇÃO DA AMOSTRA CONCLUÍDA!")


from pathlib import Path
import pandas as pd

# Pastas do projeto
PROJETO = Path(__file__).resolve().parent.parent
ORIGEM = PROJETO / "dados_originais"
DESTINO = PROJETO / "dados_tratados"
DESTINO.mkdir(parents=True, exist_ok=True)

arquivos = list(ORIGEM.rglob("RESULTADOS_2025.csv"))

if len(arquivos) != 1:
    raise FileNotFoundError(
        "Não foi encontrado exatamente um "
        "RESULTADOS_2025.csv."
    )

arquivo_original = arquivos[0]
arquivo_populacao = DESTINO / "populacao_enem_2025.csv"

# Variáveis que utilizaremos nas análises
colunas = [
    "NU_SEQUENCIAL",
    "NU_ANO",
    "SG_UF_PROVA",
    "TP_PRESENCA_MT",
    "TP_DEPENDENCIA_ADM_ESC",
    "TP_STATUS_REDACAO",
    "NU_NOTA_MT",
    "NU_NOTA_REDACAO",
    "NU_NOTA_CN",
    "NU_NOTA_CH",
    "NU_NOTA_LC"
]

total_original = 0
total_populacao = 0
primeiro_bloco = True

print("Criando população definitiva do ENEM 2025...")

for bloco in pd.read_csv(
    arquivo_original,
    sep=";",
    encoding="latin-1",
    usecols=colunas,
    dtype=str,
    chunksize=100_000
):
    total_original += len(bloco)

    # Converter notas para valores numéricos
    notas = [
        "NU_NOTA_MT",
        "NU_NOTA_REDACAO",
        "NU_NOTA_CN",
        "NU_NOTA_CH",
        "NU_NOTA_LC"
    ]

    for coluna in notas:
        bloco[coluna] = pd.to_numeric(
            bloco[coluna].str.replace(",", ".", regex=False),
            errors="coerce"
        )

    # Critério de inclusão definido no trabalho
    criterio = (
        bloco["NU_NOTA_MT"].between(0, 1000)
        & bloco["NU_NOTA_REDACAO"].between(0, 1000)
    )

    selecionados = bloco.loc[criterio].copy()
    total_populacao += len(selecionados)

    # Gravar sem carregar toda a população na memória
    selecionados.to_csv(
        arquivo_populacao,
        sep=";",
        index=False,
        mode="w" if primeiro_bloco else "a",
        header=primeiro_bloco,
        encoding="utf-8",
        decimal=","
    )

    primeiro_bloco = False

print("\nRESULTADO")
print("-------------------------------")
print(f"Registros originais: {total_original:,}")
print(f"População selecionada: {total_populacao:,}")
print(f"Registros excluídos: {total_original-total_populacao:,}")
print(f"Variáveis selecionadas: {len(colunas)}")
print(f"Arquivo gerado: {arquivo_populacao}")

# Validação final
assert total_original == 4_810_772
assert total_populacao == 3_244_348

print("\nVALIDAÇÃO CONCLUÍDA COM SUCESSO!")

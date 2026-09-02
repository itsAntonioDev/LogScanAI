import sys
from collections import Counter

CAMINHO_PADRAO = "C:/Users/meupc/Documents/Arquivos/DevOps/HtppVerify/httpverify.log"


def ler_log(caminho_arquivo):
    """Lê o arquivo e devolve a lista de linhas."""
    try:
        with open(caminho_arquivo, encoding="utf-8", errors="replace") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)


def processar_log(linhas):
    """Conta quantas linhas existem de cada nivel (INFO, WARNING, ERROR)."""
    contagem = Counter()
    erros_detalhados = []

    for linha in linhas:
        partes = linha.strip().split(" - ")
        if len(partes) < 2:
            continue

        nivel = partes[1]
        contagem[nivel] += 1

        if nivel == "ERROR":
            erros_detalhados.append(linha.strip())

    return contagem, erros_detalhados


def mostrar_relatorio(contagem, erros_detalhados, total_linhas):
    """Imprime o relatorio final formatado."""
    print("=== Relatorio de Log ===")
    print(f"Total de linhas: {total_linhas}")
    print(f"INFO: {contagem.get('INFO', 0)}")
    print(f"WARNING: {contagem.get('WARNING', 0)}")
    print(f"ERROR: {contagem.get('ERROR', 0)}")

    if erros_detalhados:
        print("\n--- Detalhes dos erros ---")
        for erro in erros_detalhados:
            print(erro)


def main():
    if len(sys.argv) >= 2:
        caminho_arquivo = sys.argv[1]
    else:
        caminho_arquivo = CAMINHO_PADRAO
        print(f"Nenhum caminho informado, usando padrao: {caminho_arquivo}\n")

    linhas = ler_log(caminho_arquivo)
    contagem, erros_detalhados = processar_log(linhas)
    mostrar_relatorio(contagem, erros_detalhados, len(linhas))


if __name__ == "__main__":
    main()
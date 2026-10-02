import os
import sys
import argparse
from collections import Counter

import requests
from dotenv import load_dotenv

load_dotenv() # loads the GEMINI_API_KEY from the .env file

CAMINHO_PADRAO = "C:/Users/meupc/Documents/Arquivos/DevOps/HtppVerify/httpverify.log"
MODELO_GEMINI = "gemini-flash-latest"


def ler_log(caminho_arquivo):
    """Lê o arquivo e devolve a lista de linhas."""
    try:
        with open(caminho_arquivo, encoding="utf-8", errors="replace") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)


def processar_log(linhas):
    """Conta as linhas por nivel e separa os ERROR e WARNING."""
    contagem = Counter()
    erros_detalhados = []
    alertas = []

    for linha in linhas:
        partes = linha.strip().split(" - ")
        if len(partes) < 2:
            continue

        nivel = partes[1]
        contagem[nivel] += 1

        if nivel == "ERROR":
            erros_detalhados.append(linha.strip())
        elif nivel == "WARNING":
            alertas.append(linha.strip())

    return contagem, erros_detalhados, alertas


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


def analisar_com_gemini(linhas_problema, modelo=MODELO_GEMINI):
    """Envia os WARNING/ERROR para o Gemini e devolve a analise."""
    if not linhas_problema:
        return "Nenhum WARNING/ERROR para analisar."

    chave = os.getenv("GEMINI_API_KEY")
    if not chave:
        return "Erro: GEMINI_API_KEY não encontrada. Confira o arquivo .env."

    logs = "\n".join(linhas_problema[-50:])  # limits the size
    prompt = (
        "Você é um engenheiro DevOps. Analise estes logs de monitoramento "
        "de sites/APIs e responda em português do Brasil:\n"
        "1) Resumo curto\n"
        "2) Causas prováveis (DNS, TCP, TLS, timeout, status HTTP)\n"
        "3) O que verificar primeiro\n\n"
        f"{logs}"
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    corpo = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        r = requests.post(url, headers={"x-goog-api-key": chave}, json=corpo, timeout=60)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.HTTPError as e:
        if r.status_code == 404:
            return f"Erro 404: modelo '{modelo}' não encontrado. Confira o nome no AI Studio."
        if r.status_code == 429:
            return "Erro 429: limite de requisições do plano grátis. Espere um pouco e tente de novo."
        return f"Erro HTTP ao consultar o Gemini: {e}"
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com o Gemini: {e}"
    except (KeyError, IndexError):
        return "Resposta inesperada do Gemini (sem texto)."


def main():
    parser = argparse.ArgumentParser(description="LogScan - analisa logs do HttpVerify")
    parser.add_argument("caminho", nargs="?", default=CAMINHO_PADRAO, help="caminho do log")
    parser.add_argument("--ai", action="store_true", help="analisa WARNING/ERROR com o Gemini")
    parser.add_argument("--modelo", default=MODELO_GEMINI, help="modelo do Gemini")
    args = parser.parse_args()

    if args.caminho == CAMINHO_PADRAO:
        print(f"Nenhum caminho informado, usando padrao: {args.caminho}\n")

    linhas = ler_log(args.caminho)
    contagem, erros_detalhados, alertas = processar_log(linhas)
    mostrar_relatorio(contagem, erros_detalhados, len(linhas))

    if args.ai:
        print("\n=== Analise da IA ===")
        print(analisar_com_gemini(alertas + erros_detalhados, args.modelo))


if __name__ == "__main__":
    main()
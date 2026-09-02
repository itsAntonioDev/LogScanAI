# LogScan

Analisador de logs em Python que lê arquivos de log, extrai o nível de severidade de cada linha (INFO, WARNING, ERROR) e gera um relatório resumido  incluindo os detalhes de cada erro encontrado.

Criado como ferramenta complementar ao [HttpVerify](https://github.com/itsAntonioDev/HttpVerify), reaproveitando os logs gerados pelo monitor de disponibilidade HTTP.

## O que ele faz

- Lê um arquivo de log linha por linha
- Identifica o nível de cada entrada (INFO, WARNING, ERROR)
- Conta quantas ocorrências existem de cada nível
- Lista os detalhes de cada erro encontrado
- Gera um relatório formatado no terminal

## Exemplo de saída

```
=== Relatorio de Log ===
Total de linhas: 22
INFO: 17
WARNING: 0
ERROR: 5

--- Detalhes dos erros ---
2026-08-25 00:12:08,472 - ERROR - Teste Fora do Ar FORA DO AR - HTTPSConnectionPool(...)
2026-08-25 00:15:17,727 - ERROR - Teste Fora do Ar FORA DO AR - HTTPSConnectionPool(...)
```

## Como usar

### Pré-requisitos

- Python 3.8 ou superior

### Rodando com o log padrão

O script já vem configurado com um caminho padrão. Basta rodar:

```bash
python3 LogScan.py
```

### Rodando com outro arquivo de log

Também é possível apontar para qualquer outro arquivo `.log`:

```bash
python3 LogScan.py "caminho/para/outro-arquivo.log"
```

## Formato de log esperado

O script espera linhas no formato:

```
DATA HORA - NIVEL - MENSAGEM
```

Exemplo:

```
2026-08-25 00:11:11,127 - INFO - Google OK - 840.13ms
```

## Estrutura do projeto

```
LogScan/
├── LogScan.py         # script principal
├── sample.log         # arquivo de log de exemplo, para testes
└── README.md
```

## Detalhes técnicos

- Tratamento de erro caso o arquivo informado não exista
- Leitura com `encoding="utf-8"` e `errors="replace"`, evitando falhas por caracteres especiais malformados no log
- Código organizado em funções (leitura, processamento e exibição), separando responsabilidades





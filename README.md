# SCURL — Structural & Contextual URL Risk Locator

> Motor heurístico de análise de risco para detecção de URLs maliciosas e suspeitas.

SCURL é um scanner baseado em análise heurística e estatística capaz de estimar o risco de URLs potencialmente maliciosas.

Ao invés de depender exclusivamente de listas de bloqueio, o SCURL analisa:

- estrutura da URL
- comportamento HTTP
- metadados DNS
- certificados SSL
- sinais contextuais
- padrões de infraestrutura

para produzir um score de risco entre `0` e `100`.

O motor heurístico permite detectar padrões suspeitos mesmo em URLs nunca vistas anteriormente.

---

![License](https://img.shields.io/badge/license-MIT-darkblue)
![Language](https://img.shields.io/badge/language-Python-black)

---

# Índice

- [Instalação](#instalação)
- [Uso](#uso)
  - [CLI](#cli)
  - [API](#api)
- [Exemplo](#exemplo)
- [Features](#features)
- [Documentação](#documentação)
- [Limitações](#limitações)
- [Licença](#licença)

---

# Instalação

## Requisitos

- Python 3.11+

---

## Clone do projeto

```bash
git clone https://github.com/JuaanReis/scurl.git
cd scurl
```

---

## Instalação

```bash
pip install -e .
```

Após a instalação:

```bash
scurl
scurl-api
```

estarão disponíveis no ambiente.

---

## Variáveis de ambiente

Crie um arquivo `.env`:

```env
GOOGLE_SAFE_BROWSING_KEY=sua_chave
SCURL_DB_PATH=./providers/database/storage/scurl.db
```

A heurística `safe_browsing` é automaticamente desativada caso nenhuma chave seja fornecida.

---

# Uso

## CLI

```bash
scurl -u "https://example.com"
```

### Exemplos

```bash
# análise simples
scurl -u "https://example.com"

# saída detalhada
scurl -u "https://example.com" -v

# salvar JSON
scurl -u "https://example.com" -o result.json

# reutilizar cache
scurl -u "https://example.com" -c
```

---

## API

Inicie o servidor:

```bash
scurl-api
```

Servidor:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

### Exemplo de request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"http://www.exemp1o.com/results?user=i123"}'
```

---

# Exemplo

```text
SCURL :: heuristic web analyzer v1.0.7
────────────────────────────────────────

Target
======
URL ............. https://maxismyclp.help
Host .................... maxismyclp.help
Registered .............. maxismyclp.help

Security Posture
================
HSTS ........................... DISABLED
CSP ............................ DISABLED

Engine
======
Rules Loaded ......................... 36
Triggered ............................. 4

Findings
========
[+] favicon externo + domínio novo
[!] domínio novo + DNS suspeito

Risk Score
==========
84.60 / 100.00
[████████░░] VERY HIGH

Assessment
==========
O alvo apresenta fortes indicadores de atividade maliciosa.
```

---

# Features

- análise estrutural de URLs
- detecção de typosquatting
- análise heurística contextual
- scoring probabilístico
- resolução de dependências entre sinais
- análise DNS
- análise SSL/TLS
- detecção de phishing patterns
- análise HTML
- cache SQLite
- API REST
- CLI formatada
- exportação JSON
- execução paralela
- integração com Google Safe Browsing

---

# Documentação

| Documento | Descrição |
|-----------|-----------|
| [`docs/architecture.md`](./docs/architecture.md) | arquitetura interna do motor |
| [`docs/heuristics.md`](./docs/heuristics.md) | heurísticas e categorias |
| [`docs/scoring.md`](./docs/scoring.md) | sistema de scoring |
| [`docs/calibration.md`](./docs/calibration.md) | calibração e limitações |
| [`docs/CLI.md`](./docs/CLI.md) | flags e uso da CLI |
| [`docs/API.md`](./docs/API.md) | endpoints REST |

---

# Limitações

O SCURL é um sistema heurístico.

Ele:

- não garante detecção absoluta
- não substitui análise humana
- pode produzir falsos positivos
- depende parcialmente de coleta externa

Atualmente o motor não executa:

- JavaScript
- browser sandbox
- rendering client-side

Mais detalhes em:

- [`docs/calibration.md`](./docs/calibration.md)

---
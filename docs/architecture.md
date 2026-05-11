# Arquitetura do SCURL

O SCURL foi projetado como um motor heurístico modular dividido em múltiplas camadas independentes. A arquitetura separa claramente:

- coleta de dados
- execução de heurísticas
- resolução contextual
- cálculo estatístico
- formatação de resposta

Essa separação permite reutilização do pipeline tanto na CLI quanto na API REST.

---

# Visão geral

```text
Client Request
      │
      ▼
Entrypoint (CLI ou API)
      │
      ▼
Pipeline
 ├─ validate_url
 ├─ collect
 ├─ execute
 ├─ context_apply
 ├─ score
 └─ response_builder
      │
      ▼
Database (SQLite)
      │
      ▼
Output
```

---

# Entrypoints

O projeto possui dois pontos de entrada independentes:

```bash
scurl
scurl-api
```

## CLI

Localizada em:

```text
app/cli/
```

Responsável por:

- parsing de argumentos
- renderização terminal
- exportação JSON
- gerenciamento de cache
- execução local

---

## API REST

Localizada em:

```text
app/api/
```

Baseada em:

- FastAPI
- Uvicorn
- Pydantic

Responsável por:

- endpoints REST
- serialização
- validação
- rate limiting
- documentação OpenAPI

---

# Pipeline de análise

## 1. validate_url

Validação e normalização da URL.

Etapas:

- validação de schema
- normalização de host
- remoção de caracteres inválidos
- parsing estrutural
- separação de query/fragment/path

Saída:

```text
ScanContext
```

---

## 2. collect

Responsável pela coleta de dados externos.

Inclui:

- requisição HTTP
- DNS lookup
- SSL inspection
- RDAP
- Safe Browsing
- redirects
- headers
- HTML bruto

A coleta é desacoplada das heurísticas para evitar múltiplas requisições redundantes.

---

## 3. execute

Execução paralela das heurísticas.

Implementado via:

```python
ThreadPoolExecutor
```

Cada heurística recebe um contexto imutável contendo:

- URL estruturada
- resposta HTTP
- metadados DNS
- SSL
- HTML parseado

Todas as heurísticas executam isoladamente.

---

## 4. context_apply

Segunda passagem responsável por aplicar dependências heurísticas.

Permite:

- reduzir scores
- amplificar sinais
- invalidar heurísticas

Esse estágio evita:

- double counting
- inflação artificial
- falsos positivos sistemáticos

---

## 5. score

Combinação estatística dos resultados heurísticos.

Processo:

1. média ponderada
2. transformação sigmoide
3. normalização 0–100
4. classificação textual

Saída:

```text
low
medium
high
critical
```

---

## 6. response_builder

Separação da resposta em:

```text
ScanResult
TargetData
```

### ScanResult

Contém:

- score
- heurísticas
- insights
- estatísticas
- metadados

### TargetData

Contém:

- URL estruturada
- headers
- redirects
- payload
- DNS
- SSL
- rede

---

# Sistema de cache

O SCURL utiliza SQLite para persistência local.

A chave de cache é:

```text
SHA-256(url_normalizada)
```

Objetivos:

- evitar reprocessamento
- acelerar análises repetidas
- permitir histórico local

---

# Modelo de execução

O pipeline é híbrido:

| Tipo | Modelo |
|------|--------|
| I/O bound | paralelo |
| CPU bound | síncrono |
| heurísticas | thread pool |
| parsing | local |

A arquitetura favorece:

- baixa latência
- alta reutilização
- isolamento de heurísticas

---

# Estrutura do projeto

```text
app/
 ├─ api/
 ├─ cli/
 └─ core/

core/
 ├─ engine/
 ├─ heuristics/
 ├─ models/
 ├─ pipeline/
 ├─ scoring/
 ├─ utils/
 └─ providers/
```
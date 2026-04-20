# SCURL

> Motor heurístico de análise de risco para detecção de URLs maliciosas e suspeitas.

**SCURL** é um scanner baseado em **análise heurística e estatística** capaz de estimar o risco de URLs potencialmente maliciosas.

Ao invés de depender exclusivamente de **listas de bloqueio**, o SCURL analisa padrões estruturais da URL, comportamento da resposta HTTP e metadados do domínio para produzir um **score de risco entre 0 e 100**.

O motor heurístico permite detectar **padrões suspeitos mesmo em URLs nunca vistas anteriormente**, tornando o sistema resistente a domínios recém-registrados e ataques zero-day de phishing.

---

![License](https://img.shields.io/badge/license-MIT-darkblue)
![Language](https://img.shields.io/badge/language-Python-black)

---

# Índice

- [Instalação](#instalação)
- [Uso](#uso)
  - [API](#api)
  - [CLI](#cli)
- [Como funciona](#como-funciona)
- [Motor de Pontuação Heurística](#motor-de-pontuação-heurística)
- [Arquitetura](#arquitetura)
- [Fluxo do scanner](#fluxo-do-scanner)
- [Colaboradores](#colaboradores)

---

# Instalação

**Pré-requisitos:** Python 3.11+

```bash
# Clone o repositório
git clone https://github.com/JuaanReis/scurl.git
cd scurl

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

---

# Uso

## API

Para analisar uma URL suspeita, envie uma requisição **POST** para o endpoint `/scan/` contendo a URL no corpo da requisição em formato JSON.

```bash
curl -X POST http://localhost:8000/scan/ \
  -H "Content-Type: application/json" \
  -d '{"url": "http://www.exemp1o.com/results?user=i123"}'
```

A resposta será um objeto **JSON** com o score de risco e os detalhes completos da análise:

```json
{
  "status": "ok",
  "engine": {
    "name": "scurl",
    "version": "0.1"
  },
  "meta": {
    "scan_id": "a3f1c2e4b5d6e7f8a9b0c1d2e3f4a5b6",
    "scan_time_s": 3.706,
    "timestamp": "2026-04-13T01:07:16.850351+00:00"
  },
  "result": {
    "score": 45.32,
    "risk_level": "medium",
    "verdict": "suspicious"
  },
  "target": {
    "url": "http://www.exemp1o.com/results?user=i123",
    "scheme": "http",
    "hostname": "www.exemp1o.com",
    "registered_domain": "exemp1o.com",
    "tld": "com",
    "subdomains": ["www"],
    "subdomain_count": 1,
    "netloc": "www.exemp1o.com",
    "is_https": false
  },
  "network": {
    "status_code": 200,
    "response_time_s": 1.243
  },
  "stats": {
    "rules_total": 26,
    "rules_triggered": 2,
    "trigger_rate": 0.077
  },
  "heuristics": [
    {
      "name": "ssl_verify",
      "category": "server",
      "value": 0.75,
      "weight": 3.5,
      "details": {
        "age_days": 9,
        "validity_days": 90,
        "san_count": 1
      }
    },
    {
      "name": "domain_entropy",
      "category": "url",
      "value": 0.5,
      "weight": 3.0,
      "details": {
        "entropy": 2.6
      }
    }
  ],
  "insight": [
    "Certificado SSL com menos de 30 dias de idade.",
    "URL utiliza HTTP sem criptografia."
  ]
}
```

### Campos da resposta

| Campo | Descrição |
|-------|-----------|
| `meta.scan_id` | Identificador único da análise |
| `meta.scan_time_s` | Tempo total de execução em segundos |
| `result.score` | Score final de risco (0–100) |
| `result.risk_level` | Classificação do nível de risco |
| `result.verdict` | Veredicto textual da análise |
| `target` | Estrutura parseada da URL analisada |
| `target.is_https` | Indica se a URL utiliza HTTPS |
| `network.status_code` | Código HTTP retornado pelo alvo |
| `network.response_time_s` | Tempo de resposta da requisição ao alvo |
| `stats.trigger_rate` | Proporção de heurísticas acionadas (`rules_triggered / rules_total`) |
| `heuristics` | Lista de heurísticas executadas com scores e detalhes |
| `insight` | Observações geradas automaticamente com base nos sinais detectados |

### Interpretação do score

| Score | Nível de risco | Significado |
|-------|---------------|-------------|
| 0 – 25 | Baixo | URL provavelmente legítima |
| 26 – 50 | Médio | Sinais ambíguos; requer atenção |
| 51 – 75 | Alto | Padrões suspeitos detectados |
| 76 – 100 | Crítico | Alta probabilidade de URL maliciosa |

> **Nota:** Heurísticas que retornam `null` indicam que o sinal é inaplicável para a URL em questão (ex: análise SSL em URLs sem HTTPS). Esses valores são excluídos do cálculo do score final para não distorcer o resultado.

---

## CLI

O SCURL também pode ser executado diretamente via linha de comando, sem necessidade de subir o servidor.

```bash
python -m cli.scurl --url "http://www.exemp1o.com/results?user=i123"
```

### Flags disponíveis

| Flag | Atalho | Tipo | Padrão | Descrição |
|------|--------|------|--------|-----------|
| `--url` | `-u` | `string` | — | URL a ser analisada |
| `--verbose` | `-v` | `bool` | `false` | Exibe detalhes completos de cada heurística |
| `--threads` | `-t` | `int` | `1` | Número de threads para análise em lote |
| `--output` | `-o` | `string` | — | Caminho para salvar o resultado em JSON |

### Exemplos

```bash
# Análise simples
python -m cli.scurl -u "http://www.exemp1o.com"

# Com saída detalhada
python -m cli.scurl -u "http://www.exemp1o.com" --verbose

# Salvar resultado em arquivo
python -m cli.scurl -u "http://www.exemp1o.com" --output resultado.json

# Análise em lote com múltiplas threads
python -m cli.scurl -u "http://www.exemp1o.com" --threads 4
```

---

# Como funciona

O **SCURL Engine** executa uma pipeline de análise heurística composta por três camadas independentes. Cada camada extrai sinais que podem indicar comportamento malicioso ou suspeito. Os sinais são normalizados e combinados para produzir um **score final de risco**.

---

## 1. Análise da estrutura da URL

A primeira etapa analisa a estrutura da URL em busca de padrões frequentemente associados a ataques de phishing e engenharia social.

Heurísticas aplicadas:

- **Entropia do domínio** — domínios gerados automaticamente (DGA) tendem a ter alta entropia de caracteres
- **Proporção de dígitos** — excesso de números no domínio é atípico em sites legítimos
- **Profundidade de subdomínios** — subdomínios excessivos são usados para simular URLs reais (ex: `paypal.login.verify.atacante.com`)
- **Presença de `@` na URL** — técnica clássica de redirecionamento enganoso
- **Codificações mistas** — percent-encoding, unicode e punycode combinados sugerem ofuscação intencional
- **Detecção de segmentos base64** — strings base64 em paths e query params frequentemente ocultam payloads ou redirecionamentos
- **Detecção de typosquatting** — similaridade com domínios conhecidos (ex: `goog1e.com`)
- **Risco de path aleatório** — entropy de Shannon e proporção de caracteres únicos para detectar hashes e tokens suspeitos

---

## 2. Análise de resposta HTTP

Após a análise estrutural, o scanner realiza uma requisição ao alvo e analisa a resposta HTTP em busca de sinais comportamentais.

Sinais analisados:

- **Cadeias de redirecionamento anormais** — múltiplos redirects encadeados são comuns em campanhas de phishing para dificultar rastreamento
- **Redirecionamento aberto** — parâmetros de query contendo URLs completas indicam possível open redirect
- **Conteúdo ofuscado** — presença de JavaScript ofuscado, iframes ocultos ou scripts de coleta de credenciais
- **Padrões estruturais de phishing** — formulários de login fora de contexto, páginas que imitam interfaces bancárias ou de grandes plataformas

---

## 3. Inteligência de domínio

O scanner coleta metadados do domínio para avaliar sua confiabilidade histórica e técnica.

Informações coletadas:

- **TTL do DNS** — domínios com TTL muito baixo (rápida rotação de IP) são suspeitos
- **Validade e idade do certificado SSL** — certificados com menos de 30 dias de idade são comuns em domínios de phishing efêmeros
- **Contagem de SANs** — certificados legítimos de grandes plataformas tipicamente possuem múltiplos SANs; certificados com SAN único e domínio suspeito são sinais negativos
- **Registros SPF e DKIM** — ausência de registros de autenticação de e-mail indica domínio não configurado para uso legítimo
- **Registros MX** — presença e consistência dos servidores de e-mail

---

# Motor de Pontuação Heurística

Cada heurística produz um **score normalizado** entre `0.0` (sem risco) e `1.0` (risco máximo), acompanhado de um **peso** que reflete sua relevância relativa.

> Heurísticas que retornam `None` indicam que o sinal é inaplicável para a URL em questão (ex: análise SSL em URLs sem HTTPS). Esses valores são excluídos do cálculo para não distorcer o resultado.

### Etapa 1 — Média ponderada

Os scores das heurísticas são combinados em uma média ponderada:

![formula](https://latex.codecogs.com/svg.image?\color{white}s=\frac{\sum(H_i\cdot%20W_i)}{\sum%20W_i})

Onde:
- `Hᵢ` é o score normalizado da heurística `i` (entre 0 e 1)
- `Wᵢ` é o peso atribuído à heurística `i`

### Etapa 2 — Função sigmoide

O score combinado `s` é transformado por uma função sigmoide para produzir o score final `Sƒ`:

![formula](https://latex.codecogs.com/svg.image?\color{white}S_f=\frac{1}{1+e^{-k(s-0{,}5)}})

Onde:
- `s` é o score combinado da etapa anterior
- `k` é o fator de sensibilidade que controla a inclinação da curva (valor padrão: `k = 5`)
- `0,5` é o ponto de inflexão — scores acima desse limiar tendem fortemente para o risco máximo
- `e` é a base do logaritmo natural `≈ 2,71828`

O resultado `Sƒ ∈ (0, 1)` é então multiplicado por 100 para produzir o score final exibido na resposta.

---

# Arquitetura (API)

A arquitetura do SCURL é dividida em módulos independentes, cada um responsável por uma etapa específica da análise.

```
Client Request
      │
      ▼
API Endpoint (FastAPI)
      │
      ▼
URL Parser
      │
      ▼
Heuristic Engine
 ├─ URL Structure Analyzer
 │    ├─ domain_entropy
 │    ├─ mixed_encoding
 │    ├─ base64_segment
 │    ├─ random_path_risk
 │    └─ query_contains_url
 ├─ HTTP Response Analyzer
 │    └─ (análise de redirects, conteúdo e comportamento)
 └─ Domain Intelligence Module
      ├─ ssl_verify
      └─ dns_verify
      │
      ▼
Score Aggregator (weighted_average → sigmoid)
      │
      ▼
Risk Scoring Engine
      │
      ▼
JSON Response
```

Essa separação permite adicionar novas heurísticas sem modificar o núcleo do sistema.

---

# Fluxo do scanner

O processo completo de análise segue o seguinte fluxo:

1. Receber URL via API
2. Realizar parsing e validação da URL
3. Executar heurísticas estruturais (análise offline, sem requisições)
4. Realizar requisição HTTP ao alvo
5. Analisar resposta do servidor
6. Coletar metadados de domínio via DNS e SSL
7. Normalizar os resultados das heurísticas
8. Calcular score final via média ponderada + sigmoide
9. Retornar resultado em JSON

---

# Colaboradores

O projeto foi desenvolvido por alunos da [**ETEC Albert Einstein**](https://www.etecalberteinstein.com.br/).

| Colaborador | Papel |
|-------------|-------|
| [Rafael Araújo Bonaldi](https://github.com/Rafzel45) | Líder do projeto, coordenação geral |
| [Juan Teixeira dos Reis](https://github.com/JuaanReis) | Desenvolvimento da API e motor heurístico |
| [Enzo Trindade da Silva](https://github.com/enzotrindade0009-byte) | Servidor WEB |
| [Raphael Gabriel Negreiro](https://github.com/rpx007) | Modelagem de BD |
| [Leonardo Alves de Souza](https://github.com/azhator1) | Design geral |
| [Igor Castilho Maia](https://github.com/IgorColinor) | Front-end WEB e Mobile |
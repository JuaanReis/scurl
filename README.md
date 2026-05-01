# SCURL — Structural & Contextual URL Risk Locator

> Motor heurístico de análise de risco para detecção de URLs maliciosas e suspeitas.

**SCURL** é um scanner baseado em **análise heurística e estatística** capaz de estimar o risco de URLs potencialmente maliciosas.

Ao invés de depender exclusivamente de **listas de bloqueio**, o SCURL analisa padrões estruturais da URL, comportamento da resposta HTTP e metadados do domínio para produzir um **score de risco entre 0 e 100**.

O motor heurístico permite detectar **padrões suspeitos mesmo em URLs nunca vistas anteriormente**.

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
- [Sistema de Dependências entre Heurísticas](#sistema-de-dependências-entre-heurísticas)
- [Arquitetura](#arquitetura)
- [Fluxo do scanner](#fluxo-do-scanner)
- [Limitações e Calibração](#limitações-e-calibração)
- [Colaboradores](#colaboradores)

---

# Instalação

**Pré-requisitos:** Python 3.11+

```bash
# Clone o repositório
git clone https://github.com/JuaanReis/scurl.git
cd scurl
```

### Com pip

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

> Mais informações em [installation](./doc/installation.md)

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
| `heuristics[].value` | Score normalizado entre `0.0` (sem risco) e `1.0` (risco máximo). `null` indica que a heurística é inaplicável para a URL em questão (ex: análise SSL em URLs sem HTTPS) e é excluída do cálculo |
| `insight` | Observações geradas automaticamente com base nos sinais detectados |

### Interpretação do score

| Score | Nível de risco | Significado |
|-------|---------------|-------------|
| 0 – 25 | Baixo | URL provavelmente legítima |
| 26 – 50 | Médio | Sinais ambíguos; requer atenção |
| 51 – 75 | Alto | Padrões suspeitos detectados |
| 76 – 100 | Crítico | Alta probabilidade de URL maliciosa |

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

> Mais informações em [CLI](./doc/CLI.md)

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
- **Codificações mistas** — percent-encoding, unicode e punycode combinados sugerem ofuscação intencional (`mixed_encoding`)
- **Detecção de segmentos base64** — strings base64 em paths e query params frequentemente ocultam payloads ou redirecionamentos (`base64_segment`)
- **Detecção de typosquatting** — similaridade com domínios conhecidos (ex: `goog1e.com`)
- **Risco de path aleatório** — entropia de Shannon e proporção de caracteres únicos para detectar hashes e tokens suspeitos (`random_path_risk`)
- **Query contendo URL** — parâmetros de query com URLs completas embutidas indicam possível open redirect ou payload encadeado (`query_contains_url`)

---

## 2. Análise de resposta HTTP

Após a análise estrutural, o scanner realiza uma requisição ao alvo e analisa a resposta HTTP em busca de sinais comportamentais.

Sinais analisados:

- **Cadeias de redirecionamento anormais** — múltiplos redirects encadeados são comuns em campanhas de phishing para dificultar rastreamento (`redirect_check`)
- **Redirecionamento aberto** — parâmetros de query contendo URLs completas indicam possível open redirect
- **Scripts externos suspeitos** — carregamento de scripts de origens externas não relacionadas ao domínio principal, identificadas por ASN (`external_script`)
- **Conteúdo ofuscado** — presença de JavaScript ofuscado, iframes ocultos ou scripts de coleta de credenciais
- **Padrões estruturais de phishing** — formulários de login fora de contexto, páginas que imitam interfaces bancárias ou de grandes plataformas
- **Risco de incompatibilidade de conteúdo** — discrepância entre o domínio anunciado e o conteúdo real da página (`content_mismatch_risk`)
- **Pré-preenchimento de campos sensíveis** — formulários com campos de credenciais pré-populados via query params (`sensitive_field_prefill`)

---

## 3. Inteligência de domínio

O scanner coleta metadados do domínio para avaliar sua confiabilidade histórica e técnica.

Informações coletadas:

- **Idade do domínio** — domínios registrados há poucos dias são fortemente associados a campanhas de phishing (`domain_age`)
- **TTL do DNS** — domínios com TTL muito baixo (rápida rotação de IP) são suspeitos (`dns_verify` → `dns_ttl`)
- **Validade e idade do certificado SSL** — certificados com menos de 30 dias de idade são comuns em domínios de phishing efêmeros (`ssl_verify` → `f_age`, `f_valid`)
- **Emissor do certificado SSL** — certificados de autoridades de baixo prestígio ou gratuitas sem histórico associado ao domínio são sinais de alerta (`f_issuer`)
- **Certificate Transparency logs** — ausência do certificado em logs públicos de CT pode indicar uso malicioso ou evasão (`f_ct`)
- **Presença de org no certificado** — certificados sem campo de organização validado são mais comuns em domínios efêmeros (`f_org`)
- **Contagem de SANs** — certificados legítimos de grandes plataformas tipicamente possuem múltiplos SANs; certificados com SAN único e domínio suspeito são sinais negativos (`f_san`)
- **Registros SPF e DKIM** — ausência de registros de autenticação de e-mail indica domínio não configurado para uso legítimo (`dns_verify` → `dns_spf`, `dns_dkim`)
- **Registros MX** — presença e consistência dos servidores de e-mail (`dns_verify` → `dns_mx`)
- **Registros A / resolução DNS** — falha na resolução ou IPs associados a infraestrutura de hosting barato são sinais contextuais (`dns_verify` → `dns_a`)

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

# Sistema de Dependências entre Heurísticas

O SCURL implementa um mecanismo de **dependências cruzadas** entre heurísticas para reduzir double-counting e evitar que sinais correlacionados inflem artificialmente o score final.

Após a execução inicial de todas as heurísticas, uma segunda passagem avalia as dependências declaradas por cada regra. Com base nos resultados de outras heurísticas, uma regra pode:

| Ação | Descrição |
|------|-----------|
| `reduce` | Reduz o score da heurística atual, pois outro sinal contextualiza o resultado como menos suspeito |
| `increase` | Amplifica o score quando outro sinal confirma ou agrava o risco |
| `skip` | Marca a heurística como inaplicável (`None`), excluindo-a do cálculo final |

### Exemplo prático

A ausência de registros MX (`dns_mx`) é um sinal de risco isolado. Porém, domínios de grandes plataformas de CDN (ex: Netlify, Cloudflare Pages, Azure Blob Storage) legitimamente não possuem infraestrutura de e-mail. Quando o contexto indica que o domínio pertence a esse tipo de plataforma, a heurística `dns_mx` pode ter seu score reduzido via dependência, evitando falsos positivos sistemáticos nesse cenário.

Esse mecanismo permite que o motor raciocine sobre **combinações de sinais**, e não apenas sobre sinais isolados.

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
 │    ├─ digit_ratio
 │    ├─ subdomain_depth
 │    ├─ at_sign_presence
 │    ├─ mixed_encoding
 │    ├─ base64_segment
 │    ├─ typosquatting
 │    ├─ random_path_risk
 │    └─ query_contains_url
 │
 ├─ HTTP Response Analyzer
 │    ├─ redirect_check
 │    ├─ external_script
 │    ├─ content_mismatch_risk
 │    └─ sensitive_field_prefill
 │
 └─ Domain Intelligence Module
      ├─ domain_age
      ├─ ssl_verify (f_age, f_valid, f_san, f_issuer, f_ct, f_org)
      └─ dns_verify (dns_mx, dns_ttl, dns_spf, dns_dkim, dns_a)
            │
            ▼
Dependency Resolution (2ª passagem: reduce / increase / skip)
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
7. Executar resolução de dependências entre heurísticas
8. Normalizar os resultados das heurísticas
9. Calcular score final via média ponderada + sigmoide
10. Retornar resultado em JSON

---

# Limitações e Calibração

O SCURL é um sistema heurístico — por definição, não é infalível. As seções a seguir documentam as limitações conhecidas e os resultados de calibração observados durante o desenvolvimento.

## Falsos positivos conhecidos

Certas categorias de URLs legítimas tendem a acumular sinais de risco por razões estruturais, não por comportamento malicioso:

**Plataformas de hosting estático (Netlify, Cloudflare Pages, Azure Blob Storage, Framer)**
Esses domínios frequentemente não possuem registros MX, DKIM ou SPF, pois não são configurados para envio de e-mail. Além disso, dados WHOIS costumam ser indisponíveis ou anonimizados. O motor pode penalizar esses domínios injustamente sem contexto adicional.

**Domínios CDN-only**
Domínios que servem exclusivamente conteúdo estático via CDN não possuem infraestrutura de e-mail e podem apresentar TTLs baixos por design de arquitetura, não por intenção maliciosa.

## Resultados de calibração

Os valores abaixo foram obtidos durante testes com URLs reais:

| Alvo | Score observado | Observação |
|------|----------------|------------|
| google.com | ~7% | Referência de baixo risco |
| youtube.com | ~13–21% | Variação por path analisado |
| instagram.com | ~15% | Ausência de MX contribui levemente |
| Phishing confirmado | 74–84% | OpenPhish / PhishTank |

## Embasamento técnico

As heurísticas implementadas são fundamentadas em literatura de segurança e detecção de ameaças:

- **Entropia de Shannon** aplicada a domínios é técnica estabelecida para detecção de DGA (Domain Generation Algorithms)
- **Análise de certificados SSL** segue padrões documentados em estudos de infraestrutura de phishing efêmero
- **Typosquatting detection** é baseada em distância de edição (Levenshtein) contra listas de domínios de referência (Tranco, Majestic Million)
- **Análise de registros DNS** (MX, SPF, DKIM) é amplamente utilizada em sistemas anti-spam e anti-phishing corporativos

---

# Colaboradores

O projeto foi desenvolvido um alunos da [**ETEC Albert Einstein**](https://www.etecalberteinstein.com.br/).

| Colaborador | Papel |
|-------------|-------|
| [Juan Teixeira dos Reis](https://github.com/JuaanReis) | Desenvolvimento da API e motor heurístico |
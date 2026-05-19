# scurl API Reference

## Base URL
 
```
https://scurl.vercel.app
```
 
---
 
## Autenticação
 
Nenhuma. A API é pública com rate limiting por IP.

---

## Rate Limiting

Configurável via `config["rate_limit"]`. Quando excedido retorna `429 Too Many Requests` com corpo padrão do SlowAPI.

Concorrência máxima: **20 scans simultâneos**. Se o semáforo estiver lotado, retorna `503` imediatamente sem enfileirar.

---

## Endpoints

### `POST /analyze`

Executa um scan heurístico completo em uma URL.

**Request**

```http
POST /analyze
Content-Type: application/json
```

```json
{
  "url": "https://example.com",
  "use_cache": false
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `url` | `HttpUrl` | sim | URL alvo. Validada pelo Pydantic. |
| `use_cache` | `bool` | não | Se `true`, busca resultado anterior no SQLite antes de escanear. Default: `false`. |

**Response `200 OK`**

```json
{
  "scan": { ... },
  "target": { ... }
}
```

Ver seções [ScanResponse](#scanresponse) e [TargetResponse](#targetresponse).

**Erros**

| Status | Condição |
|---|---|
| `400` | Engine retornou `status: "error"` |
| `422` | URL inválida (Pydantic) |
| `429` | Rate limit excedido |
| `503` | 20 scans já em execução |

---

### `GET /scans`

Lista scans armazenados no banco (requer `--cache` ativo nas execuções).

**Query Parameters**

| Parâmetro | Tipo | Default | Limites |
|---|---|---|---|
| `limit` | `int` | `50` | 1–200 |
| `offset` | `int` | `0` | ≥ 0 |

**Response `200 OK`**

```json
{
  "status": "ok",
  "total": 2,
  "scans": [
    {
      "url": "https://example.com",
      "score": 12.4,
      "risk_level": "low",
      "verdict": "safe",
      "scan_id": "abc123",
      "timestamp": "2026-05-19T03:01:58.423324+00:00",
      "url_hash": "e1d5e2c7..."
    }
  ]
}
```

---

### `GET /scans/{identifier}`

Retorna um scan completo por `scan_id` ou `url_hash`.

**Path Parameter**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `identifier` | `str` | `scan_id` (UUID hex) ou `url_hash` (SHA-256 hex) |

**Response `200 OK`**

Mesmo schema de `POST /analyze` — objeto `AnalyzeResponse` completo.

**Erros**

| Status | Condição |
|---|---|
| `404` | Identifier não encontrado no banco |

---

### `GET /health`

Health check.

**Response `200 OK`**

```json
{
  "status": "ok",
  "version": "1.0.9"
}
```

---

## Schemas

### ScanResponse

```json
{
  "status": "ok",
  "engine": {
    "name": "scurl",
    "version": "1.0.9"
  },
  "meta": {
    "scan_id": "13b0b10d192544f88b29755f7d9fbf16",
    "scan_time_s": 0.911,
    "url_hash": "e1d5e2c7...",
    "url": "https://youtube.com/",
    "threads": 2,
    "timestamp": "2026-05-19T03:01:58.423324+00:00"
  },
  "result": {
    "score": 7.8,
    "risk_level": "very low",
    "verdict": "safe"
  },
  "stats": {
    "rules_total": 36,
    "rules_triggered": 3,
    "trigger_rate": 0.083
  },
  "heuristics": [ ... ],
  "insight": []
}
```

#### `result.risk_level`

Derivado do `score` (0–100):

| Score | `risk_level` |
|---|---|
| 0–20 | `very low` |
| 21–40 | `low` |
| 41–60 | `medium` |
| 61–80 | `high` |
| 81–100 | `very high` |

#### `heuristics[]`

Cada item representa uma regra que produziu resultado.

```json
{
  "name": "ssl_score",
  "category": "server",
  "value": 0.0,
  "weight": 3.5,
  "contribution": 0.0,
  "details": { ... },
  "reasons": ["..."]
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `name` | `str` | Identificador da regra |
| `category` | `str` | `server`, `html`, `url`, `domain` |
| `value` | `float` | Score bruto da regra (0.0–1.0) |
| `weight` | `float` | Peso da regra no pipeline |
| `contribution` | `float` | Contribuição ponderada no score final |
| `details` | `dict` | Dados coletados pela regra (varia por regra) |
| `reasons` | `list[str]` | Explicações geradas pela regra |

Regras que retornam `None` (sinal não aplicável) **não aparecem** nesta lista.

---

### TargetResponse

Dados coletados sobre o alvo. Dividido em 6 seções:

#### `identity`

Decomposição da URL.

| Campo | Tipo | Descrição |
|---|---|---|
| `original_url` | `str` | URL como fornecida |
| `final_url` | `str\|null` | URL após redirecionamentos |
| `scheme` | `str` | `http` ou `https` |
| `hostname` | `str` | Host extraído |
| `registered_domain` | `str` | Domínio registrado (ex: `youtube.com`) |
| `tld` | `str` | TLD (ex: `com`) |
| `subdomains` | `list[str]` | Lista de subdomínios |
| `subdomain_count` | `int` | Quantidade de subdomínios |
| `port` | `int\|null` | Porta explícita na URL |
| `path` | `str` | Path da URL |
| `query` | `str` | Query string |
| `fragment` | `str` | Fragment (`#...`) |
| `normalized_url` | `str` | URL normalizada |
| `punycode` | `str` | Domínio em punycode |
| `unicode_domain` | `str` | Domínio em unicode |
| `is_idn` | `bool` | Internationalized Domain Name |
| `is_homograph` | `bool` | Ataque homograph detectado |
| `domain_length` | `int` | Comprimento do domínio |
| `domain_entropy` | `float` | Entropia de Shannon do domínio |
| `url_length` | `int` | Comprimento total da URL |
| `has_ip` | `bool` | URL contém IP em vez de domínio |
| `has_port` | `bool` | URL contém porta explícita |

#### `network`

| Campo | Tipo | Descrição |
|---|---|---|
| `ipv4` | `list[str]` | Endereços IPv4 resolvidos |
| `ipv6` | `list[str]` | Endereços IPv6 resolvidos |
| `reverse_dns` | `str\|null` | PTR record |
| `asn` | `{number, organization}\|null` | Autonomous System Number |
| `geo` | `{country, region, city}\|null` | Geolocalização |
| `isp` | `str\|null` | Provedor de internet |
| `cdn` | `{detected, provider}\|null` | CDN detectado |
| `waf` | `{detected, provider}\|null` | WAF detectado |
| `http_version` | `str\|null` | Versão HTTP (ex: `HTTP/2`) |
| `timings` | `Timings` | Breakdown de latência em ms |

**`timings`**

| Campo | Descrição |
|---|---|
| `total_ms` | Tempo total da requisição |
| `dns_ms` | Tempo de resolução DNS |
| `tcp_ms` | Tempo de handshake TCP |
| `tls_ms` | Tempo de handshake TLS |
| `ttfb_ms` | Time to First Byte |

#### `tls`

| Campo | Tipo | Descrição |
|---|---|---|
| `enabled` | `bool` | HTTPS ativo |
| `version` | `str\|null` | Ex: `TLSv1.3` |
| `cipher_suite` | `str\|null` | Ex: `TLS_AES_256_GCM_SHA384` |
| `issuer` | `str\|null` | Nome curto da CA |
| `issuer_detail` | `dict\|null` | `countryName`, `organizationName`, `commonName` |
| `subject` | `str\|null` | CN do certificado |
| `valid_from` | `str\|null` | Data início (`YYYY-MM-DD`) |
| `valid_until` | `str\|null` | Data expiração (`YYYY-MM-DD`) |
| `validity_days` | `int\|null` | Validade total em dias |
| `san` | `list[str]` | Subject Alternative Names |
| `san_count` | `int` | Quantidade de SANs |
| `wildcard` | `bool` | Certificado wildcard |
| `self_signed` | `bool` | Certificado auto-assinado |
| `serial_number` | `str\|null` | Serial hex |
| `signature_algorithm` | `str\|null` | Ex: `SHA256` |
| `public_key_algorithm` | `str\|null` | Ex: `EC-secp256r1` |
| `ocsp_stapling` | `bool\|null` | OCSP stapling ativo |
| `ocsp_reachable` | `bool\|null` | OCSP responder acessível |
| `fingerprints` | `{sha1, sha256}\|null` | Fingerprints do certificado |

#### `dns`

| Campo | Tipo | Descrição |
|---|---|---|
| `a` | `list[str]` | Records A |
| `aaaa` | `list[str]` | Records AAAA |
| `mx` | `list[{priority, host}]` | Records MX |
| `ns` | `list[str]` | Nameservers |
| `cname` | `list[str]` | Records CNAME |
| `txt` | `list[str]` | Records TXT |
| `spf` | `bool` | SPF configurado |
| `dmarc` | `bool` | DMARC configurado |
| `dkim` | `bool\|null` | DKIM detectado |
| `ttl` | `int\|null` | TTL em segundos |
| `has_mx` | `bool` | MX record presente |

#### `http`

| Campo | Tipo | Descrição |
|---|---|---|
| `status_code` | `int\|null` | HTTP status da resposta final |
| `response_time_s` | `float\|null` | Tempo de resposta em segundos |
| `redirects` | `int` | Número de redirecionamentos |
| `redirect_chain` | `list[{url, status, location}]\|null` | Cadeia de redirecionamentos |
| `content_type` | `str\|null` | Content-Type header |
| `content_length` | `int\|null` | Tamanho do body em bytes |
| `encoding` | `str\|null` | Content-Encoding |
| `compression` | `{enabled, algorithm}\|null` | Compressão usada |
| `server` | `str\|null` | Server header |
| `alt_svc` | `str\|null` | Alt-Svc header (HTTP/3) |
| `keep_alive` | `bool` | Keep-Alive ativo |
| `security_headers` | `dict[str, str]` | Headers de segurança presentes |
| `cookies` | `any\|null` | Cookies da resposta |

#### `content`

Análise do HTML. Campos zerados em SPAs que não renderizam server-side.

| Campo | Tipo | Descrição |
|---|---|---|
| `title` | `str\|null` | Tag `<title>` |
| `language` | `str\|null` | Atributo `lang` do `<html>` |
| `html_size_kb` | `float` | Tamanho do HTML em KB |
| `scripts` | `{total, external, inline}` | Contagem de scripts |
| `stylesheets` | `int` | Contagem de `<link rel="stylesheet">` |
| `iframes` | `int` | Contagem de `<iframe>` |
| `forms` | `{count, password_fields}` | Formulários e campos senha |
| `inputs` | `int` | Total de `<input>` |
| `images` | `int` | Total de `<img>` |
| `anchors` | `int` | Total de `<a>` |
| `favicon` | `str\|null` | URL do favicon |
| `canonical` | `str\|null` | URL canonical |
| `meta_tags` | `dict[str, str\|null]` | Meta tags relevantes |
| `generator` | `str\|null` | Meta generator (ex: WordPress) |
| `spa` | `bool` | Site detectado como SPA |
| `html_sha256` | `str\|null` | Hash do HTML para comparação |

#### `domain`

| Campo | Tipo | Descrição |
|---|---|---|
| `registrar` | `str\|null` | Registrar do domínio |
| `created_at` | `str\|null` | Data de criação (`YYYY-MM-DD`) |
| `updated_at` | `str\|null` | Última atualização |
| `expires_at` | `str\|null` | Data de expiração |
| `age_days` | `int\|null` | Idade do domínio em dias |
| `status` | `list[str]` | Status EPP do domínio |

---

### ErrorResponse

Retornado com `400` quando o engine falha internamente.

```json
{
  "status": "error",
  "meta": {
    "url": "https://example.com",
    "scan_time_s": 0.12,
    "version": "1.0.9"
  },
  "error": {
    "type": "connection_error",
    "message": "..."
  }
}
```

---

## Exemplo completo

```bash
curl -X POST https://scurl.vercel.app/analyze \
  -H "Content-Type: application/json" \
  -d @body.json
```

`body.json`:
```json
{
  "url": "https://example.com",
  "use_cache": false
}
```
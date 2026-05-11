# Heurísticas do SCURL

O SCURL utiliza um conjunto de heurísticas independentes organizadas em categorias funcionais.

Cada heurística produz:

- um score normalizado (`0.0 → 1.0`)
- metadados opcionais
- razões contextuais
- dependências opcionais

---

# Categorias

| Categoria | Objetivo |
|-----------|----------|
| URL | análise estrutural |
| HTML | comportamento da página |
| SERVER | infraestrutura e reputação |

---

# Estrutura de uma heurística

Todas as heurísticas seguem o mesmo contrato lógico:

```python
{
    "name": "ssl_score",
    "category": "server",
    "value": 0.74,
    "weight": 3.5,
    "contribution": 2.6,
    "details": {},
    "reasons": []
}
```

---

# Heurísticas de URL

## typosquatting

Detecta similaridade entre domínios suspeitos e marcas conhecidas.

Técnicas utilizadas:

- distância de Levenshtein
- normalização Unicode
- homóglifos
- Tranco Top 7000

Exemplos:

```text
paypa1.com
micr0soft-login.com
gmai1-security.net
```

---

## mixed_encoding

Detecta mistura de:

- percent encoding
- unicode
- punycode
- caracteres invisíveis

Objetivo:

identificar ofuscação intencional.

---

## random_domain_risk

Aplica entropia de Shannon no domínio.

Detecta:

- DGA
- domínios aleatórios
- hashes
- strings automatizadas

---

## query_contains_url

Detecta URLs embutidas em query params.

Exemplo:

```text
redirect=https://malicioso.com
```

Comum em:

- open redirect
- tracking abusivo
- phishing encadeado

---

# Heurísticas HTML

## form_action_check

Detecta formulários enviando dados para domínio externo.

Exemplo:

```html
<form action="https://attacker.com/login">
```

---

## favicon_check

Detecta favicon carregado externamente.

Frequente em:

- phishing kits
- clones de identidade visual

---

## password_input_check

Detecta campos de senha.

A heurística isoladamente possui baixo peso contextual.

O score aumenta quando combinado com:

- domínio novo
- typosquatting
- favicon externo

---

## missing_form_tag

Detecta inputs de credenciais fora de `<form>`.

Comum em:

- captura via JavaScript
- phishing moderno
- exfiltração dinâmica

---

# Heurísticas SERVER

## domain_age

Avalia idade do domínio.

Domínios recém registrados possuem alta correlação com:

- phishing
- malware
- campanhas efêmeras

---

## dns_score

Combina múltiplos sinais DNS:

- MX
- SPF
- DKIM
- TTL
- consistência

---

## ssl_score

Analisa:

- idade do certificado
- validade
- issuer
- SAN count
- CT logs
- organização

---

## safe_browsing

Consulta Google Safe Browsing API v4.

Categorias verificadas:

- malware
- phishing
- unwanted software
- harmful applications

---

# Sistema de dependências

As heurísticas podem depender de outras heurísticas.

Exemplo:

```text
password_input_check
    +
favicon_check
    +
domain_age
```

Resultado:

```text
increase
```

---
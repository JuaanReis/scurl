# Calibração e Limitações

O SCURL é um sistema heurístico probabilístico.

Por definição:

- não é determinístico
- não substitui análise humana
- não elimina falsos positivos
- não garante detecção absoluta

O objetivo do motor é maximizar:

- contextualização
- interpretabilidade
- generalização
- detecção de padrões

---

# Filosofia de calibração

A calibração do SCURL busca equilibrar:

| Objetivo | Impacto |
|----------|---------|
| Sensibilidade | detectar ameaças |
| Conservadorismo | reduzir falsos positivos |

O sistema prioriza:

```text
redução de falsos positivos críticos
```

especialmente em:

- CDNs
- hosting estático
- plataformas serverless
- serviços edge

---

# Baselines observados

## Baixo risco

| Domínio | Faixa observada |
|----------|----------------|
| google.com | 7–13 |
| github.com | 8–15 |
| wikipedia.org | 5–12 |

---

## Médio risco

| Cenário | Score típico |
|---------|--------------|
| domínio recém criado | 30–45 |
| múltiplos redirects | 35–50 |
| tracking agressivo | 28–44 |

---

## Alto risco

| Cenário | Score típico |
|---------|--------------|
| phishing confirmado | 74–87 |
| typosquatting + password | 80+ |
| clone visual + domínio novo | 85+ |

---

# Casos conhecidos de falsos positivos

## Plataformas estáticas

Serviços como:

- Netlify
- Vercel
- Cloudflare Pages
- Framer

frequentemente:

- não possuem MX
- possuem SPF ausente
- utilizam edge/CDN
- possuem TTL baixo

Esses sinais são parcialmente mitigados por dependências heurísticas.

---

## CDNs

Infraestruturas CDN podem apresentar:

- TTL extremamente baixo
- múltiplos IPs
- respostas dinâmicas
- headers variáveis

Isso não implica comportamento malicioso.

---

## Domínios técnicos

Painéis administrativos, APIs e serviços internos podem:

- usar paths aleatórios
- conter tokens
- utilizar querys extensas
- empregar encoding misto

O contexto operacional deve ser considerado.

---

# Limitações do Safe Browsing

A API pública do Google Safe Browsing possui:

- delay de atualização
- cobertura parcial
- limitação de quota

A heurística:

```text
safe_browsing
```

é complementar.

Ela não substitui análise estrutural.

---

# Limitações arquiteturais

## Dependência de coleta externa

Algumas heurísticas dependem de:

- DNS
- RDAP
- SSL
- requisições HTTP

Falhas de rede podem reduzir precisão contextual.

---

## Conteúdo dinâmico

O SCURL atualmente não executa:

- JavaScript
- DOM runtime
- browser sandbox
- rendering completo

Portanto:

- conteúdo carregado dinamicamente
- phishing renderizado client-side
- lógica pós-load

podem não ser totalmente analisados.

---

# Interpretação recomendada

| Score | Interpretação |
|------|---------------|
| 0–25 | baixo risco |
| 26–50 | revisar contexto |
| 51–75 | sinais suspeitos |
| 76–100 | forte convergência heurística |

---
# SCURL

> Heuristic URL risk engine for detecting malicious and suspicious web
> targets.

**SCURL** é um scanner baseado em **análise heurística e estatística**
capaz de estimar o risco de URLs potencialmente maliciosas.

Ao invés de depender exclusivamente de **listas de bloqueio**, o SCURL
analisa padrões estruturais da URL, comportamento da resposta HTTP e
metadados do domínio para produzir um **score de risco**.

------------------------------------------------------------------------

![License](https://img.shields.io/badge/license-MIT-darkblue)
![Language](https://img.shields.io/badge/language-Python-black)

------------------------------------------------------------------------

# Índice

-   [Uso](#uso)
-   [Como funciona](#como-funciona)
-   [Arquitetura](#arquitetura)
-   [Fluxo do scanner](#fluxo-do-scanner)
-   [Colaboradores](#colaboradores)

------------------------------------------------------------------------

# Uso

Para analisar uma URL suspeita, envie uma requisição **POST** para o endpoint
`/scan/` contendo a URL no corpo da requisição em formato JSON.

``` bash
curl -X POST https://www.scurl.com/scan/ \
-H "Content-Type: application/json" \
-d '{"url": "http://www.exemp1o.com/results?user=i123"}'
```

A resposta será um objeto **JSON** contendo o score de risco calculado
pelo motor heurístico.

``` json
      "status": "ok",
      "engine": {
            "name": "scurl",
            "version": "0.1"
      },
      "meta": {
            "url": "http://www.exemp1o.com/results?user=i123",
            "scan_time_s": 3.706,
            "timestamp": "2026-04-13T01:07:16.850351+00:00",
      },
      "result": {
            "score": 75.32,
            "risk_level": "high",
            "verdict": "suspicious"
      },
      "stats": {
            "rules_total": 26,
            "rules_triggered": 2
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
      ]

```

------------------------------------------------------------------------

# Como funciona

O **SCURL Engine** executa uma pipeline de análise heurística composta
por múltiplas camadas.

Cada camada extrai sinais que podem indicar comportamento malicioso ou
suspeito.

Os sinais são normalizados e combinados para produzir um **score final
de risco**.

------------------------------------------------------------------------

## 1. URL Structure Analysis

A primeira etapa analisa a estrutura da URL em busca de padrões
frequentemente associados a ataques.

Alguns exemplos de heurísticas aplicadas:

-   proporção de números na URL
-   quantidade de hífens
-   profundidade de subdomínios
-   presença de `@`
-   codificações mistas (percent-encoding, unicode, punycode)
-   entropia da string
-   similaridade com domínios legítimos (typosquatting)

Essas regras ajudam a detectar URLs geradas automaticamente ou
projetadas para enganar usuários.

------------------------------------------------------------------------

## 2. HTTP Response Analysis

Após a análise estrutural, o scanner realiza uma requisição ao alvo e
analisa a resposta HTTP.

Alguns sinais analisados:

-   cadeias anormais de redirecionamento
-   páginas intermediárias suspeitas
-   conteúdo ofuscado
-   padrões comuns em páginas de phishing

------------------------------------------------------------------------

## 3. Domain Intelligence

O scanner também coleta metadados do domínio analisado.

Entre eles:

-   idade do domínio
-   presença de SSL
-   características comuns de domínios recém registrados

------------------------------------------------------------------------

# Heuristic Scoring Engine

Cada heurística gera um **score normalizado**.

O motor de decisão então combina esses valores usando um sistema de
**pesos heurísticos**:  

![formula](https://latex.codecogs.com/svg.image?\color{white}s=\frac{\sum(H_i\cdot%20Wi)}{\sum%20Wi})

Onde:
-   `Hᵢ` é o score da heurística `i`
-   `Wᵢ` é o peso atribuído à heurística `i`

E logo depois:

![formula](https://latex.codecogs.com/svg.image?\color{white}s_f=\frac{1}{1+e^{-k\left(s-0,7\right)}})

onde:
-   `s` é o score combinado das heurísticas
-   `k` é um fator de ajuste para controlar a sensibilidade
-   `0,7` é o ponto de inflexão da função sigmoide
-   `e` é a base do logaritmo natural `≈ 2.71828`

O resultado final `𝑆𝑓` representa um **score estimado da URL ser
maliciosa ou suspeita**.

------------------------------------------------------------------------

# Arquitetura

A arquitetura do SCURL é dividida em módulos independentes responsáveis
por etapas específicas da análise.

    Client Request
          │
          ▼
    API Endpoint
          │
          ▼
    URL Parser
          │
          ▼
    Heuristic Engine
     ├─ URL Structure Analyzer
     ├─ HTTP Response Analyzer
     └─ Domain Intelligence Module
          │
          ▼
    Score Normalizer
          │
          ▼
    Risk Scoring Engine
          │
          ▼
    JSON Response

Essa separação permite adicionar novas heurísticas sem modificar o
núcleo do sistema.

------------------------------------------------------------------------

# Fluxo do scanner

O processo completo de análise segue o seguinte fluxo:

1.  Receber URL via API
2.  Realizar parsing da URL
3.  Executar heurísticas estruturais
4.  Realizar requisição HTTP ao alvo
5.  Analisar resposta do servidor
6.  Coletar metadados do domínio
7.  Normalizar os resultados das heurísticas
8.  Calcular score final de risco
9.  Retornar resultado em JSON

------------------------------------------------------------------------

# Observação

SCURL não depende exclusivamente de assinaturas conhecidas.\
O motor heurístico permite detectar **padrões suspeitos mesmo em URLs
nunca vistas anteriormente**.


# Colaboradores

O projeto foi desenvolvido por alunos da [**ETEC Albert Einstein**](https://www.etecalberteinstein.com.br/).

Mesmo que nem todos tenham participado diretamente da implementação da API, todos contribuíram para o desenvolvimento geral do projeto, incluindo pesquisa, testes, documentação e suporte técnico.

- [Rafael Araújo Bonaldi](https://github.com/Rafzel45) — Líder do projeto
- [Juan Teixeira dos Reis](https://github.com/JuaanReis) — Desenvolvimento da API e motor heurístico
- [Enzo Trindade da Silva](https://github.com/enzotrindade0009-byte)
- [Raphael Gabriel Negreiro](https://github.com/rpx007)
- [Leonardo Alves de Souza](https://github.com/azhator1)
- [Igor Castilho Maia](https://github.com/IgorColinor)
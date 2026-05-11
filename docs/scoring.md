# Sistema de Scoring

O SCURL utiliza um modelo híbrido baseado em:

- média ponderada
- transformação sigmoide
- resolução contextual

O objetivo é evitar decisões binárias simplistas e produzir um score probabilístico interpretável.

---

# Modelo geral

Cada heurística produz:

```text
0.0 → sem risco
1.0 → risco máximo
```

Além do valor bruto, cada regra possui um peso relativo.

---

# Média ponderada

```math
s = \frac{\sum(H_iW_i)}{\sum W_i}
```

Onde:

- `Hᵢ` → valor da heurística
- `Wᵢ` → peso da heurística

---

# Problema da linearidade

Modelos puramente lineares possuem limitações:

- sinais moderados acumulam risco excessivamente
- pequenas diferenças geram pouca separação
- scores extremos são raros

Para resolver isso, o SCURL aplica uma transformação sigmoide.

---

# Função sigmoide

```math
S_f = \frac{1}{1 + e^{-k(s-0.5)}}
```

Objetivos:

- ampliar separação entre baixo e alto risco
- suavizar regiões intermediárias
- aumentar interpretabilidade

---

# Parâmetro k

O fator `k` controla a sensibilidade da curva.

Valores maiores:

- aumentam agressividade
- amplificam diferenças
- tornam o sistema mais sensível

Valor padrão:

```text
k = 5
```

---

# Ponto de inflexão

O valor:

```text
0.5
```

representa o centro da curva.

Acima desse ponto:

- o score cresce rapidamente

Abaixo:

- o crescimento desacelera

---

# Conversão final

O resultado final é convertido para:

```text
0 → 100
```

Exemplo:

| Valor interno | Score final |
|---------------|-------------|
| 0.08 | 8 |
| 0.43 | 43 |
| 0.81 | 81 |

---

# Dependências contextuais

Antes do cálculo final, o motor executa resolução contextual.

As dependências podem:

| Ação | Efeito |
|------|--------|
| reduce | reduz score |
| increase | aumenta score |
| skip | remove heurística |

---

# Conservadorismo

Quando há conflito entre:

- reduce
- increase

o sistema prioriza:

```text
reduce
```

Objetivo:

reduzir falsos positivos sistemáticos.

---
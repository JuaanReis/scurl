# Uso via CLI

O **SCURL** também pode ser executado diretamente pela **linha de comando**, sem a necessidade de iniciar o servidor web.
Esse modo é útil para automação, scripts, pipelines de análise ou execução rápida no terminal.

A CLI executa o mecanismo de análise diretamente no sistema, processando a URL fornecida e exibindo o relatório no terminal.

---

# Execução básica

Para executar o SCURL via CLI, utilize o comando:

```bash
python -m cli.scurl --url "http://www.exemplo.com"
```

Ou usando o argumento posicional:

```bash
python -m cli.scurl "http://www.exemplo.com"
```

Ambas as formas são equivalentes.

---

# Flags disponíveis

| Flag        | Atalho | Tipo    | Padrão  | Descrição                                                 |
| ----------- | ------ | ------- | ------- | --------------------------------------------------------- |
| `--url`     | `-u`   | string  | —       | URL que será analisada                                    |
| `target`    | —      | string  | —       | URL passada como argumento posicional                     |
| `--verbose` | `-v`   | boolean | `false` | Mostra explicações detalhadas de cada heurística aplicada |
| `--threads` | `-t`   | inteiro | `1`     | Número de threads utilizadas na análise                   |
| `--output`  | `-o`   | string  | —       | Caminho para salvar o resultado da análise em JSON        |
| `--timeout` | `-T`   | float   | `5`     | Tempo máximo de espera para requisições HTTP              |
| `-k`        | —      | inteiro | `5`     | Parâmetro interno usado no motor de análise               |
| `--retries` | `-r`   | inteiro | `3`     | Número de tentativas caso uma requisição falhe            |

---

# Desempenho

O parâmetro `--threads` controla o número de análises executadas em paralelo.

Valores maiores podem melhorar a velocidade, mas também aumentam o consumo de:

- CPU
- conexões HTTP
- memória

## Recomendações

| Threads | Cenário |
|------|------|
| 1 | análise simples |
| 2–4 | uso normal |
| 8+ | análise em lote |

---

# Observação sobre URL

A URL pode ser fornecida de duas formas:

### Usando flag

```bash
python -m cli.scurl --url "http://site.com"
```

### Usando argumento posicional

```bash
python -m cli.scurl "http://site.com"
```

**Importante:**
Não é permitido usar os dois ao mesmo tempo. Caso isso ocorra, o programa retornará erro.

---

# Exemplos de uso

## Análise simples

Executa a análise padrão da URL.

```bash
python -m cli.scurl -u "http://www.exemplo.com"
```

---

## Saída detalhada

Mostra explicações adicionais sobre cada heurística que contribuiu para o resultado.

```bash
python -m cli.scurl -u "http://www.exemplo.com" --verbose
```

No modo `verbose`, o SCURL exibirá:

* motivo da ativação de cada regra
* fatores que influenciaram a pontuação
* observações adicionais geradas pelo motor de análise

---

## Definindo múltiplas threads

Permite executar a análise usando múltiplas threads.

```bash
python -m cli.scurl -u "http://www.exemplo.com" --threads 4
```

Isso pode melhorar o desempenho em análises mais pesadas.

---

## Definindo timeout de requisição

Controla o tempo máximo de espera por respostas HTTP.

```bash
python -m cli.scurl -u "http://www.exemplo.com" --timeout 10
```

---

## Definindo número de tentativas

Caso uma requisição falhe, o SCURL pode tentar novamente automaticamente.

```bash
python -m cli.scurl -u "http://www.exemplo.com" --retries 5
```

---

## Salvando o resultado em arquivo

Permite exportar o resultado da análise em formato **JSON**.

```bash
python -m cli.scurl -u "http://www.exemplo.com" --output resultado.json
```

Após a execução, o arquivo será salvo no caminho especificado.

---

## Enviando saída JSON para stdout

Se o valor `-` for usado como saída, o JSON será enviado diretamente para o terminal.

```bash
python -m cli.scurl -u "http://www.exemplo.com" -o-
```

Esse modo é útil para:

* integração com scripts
* pipelines de análise
* processamento com outras ferramentas

Exemplo:

```bash
python -m cli.scurl -u "http://site.com" -o- | jq
```

---

# Estrutura da saída

A CLI exibe no terminal um relatório contendo:

* módulos analisados
* regras aplicadas
* valores calculados
* peso de cada heurística
* contribuição para o score final
* observações do sistema

Exemplo de saída simplificada:

```
MÓDULO   REGRA        VALOR   PESO  CONTRIB
SERVER   ssl_verify   0.12    3.5     0.42
URL      entropy      2.87    2.1     0.30

Pontuação: 40.3  Risco: MÉDIO  Veredito: SUSPEITO
Scurl concluído: 37 regras testadas, 8 disparadas — finalizado em 1.42s
```

---

# Quando usar a CLI

O modo CLI é recomendado para:

* automação de análises
* uso em scripts
* integração com pipelines
* execução rápida sem interface web
* análise de múltiplas URLs em ambientes de linha de comando
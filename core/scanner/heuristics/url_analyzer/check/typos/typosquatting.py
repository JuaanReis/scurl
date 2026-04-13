from core.models.result_base import ResultBase
from core.scanner.heuristics.url_analyzer.check.typos.wordlists.wordlist_generator import domain_generator as load_domains
from core.scanner.heuristics.url_analyzer.check.typos.index import build_index
from core.scanner.heuristics.url_analyzer.check.typos.detect import detect

domains = list(load_domains("./core/wordlists/hostnames_1m.txt"))
BY_LEN, BY_FIRST = build_index(domains)

def extract_domain(url: str) -> str:
    host = url.split("//")[-1].split("/")[0]
    parts = host.split(".")

    if len(parts) >= 2:
        return parts[-2]

    return host
   
def typosquatting(structure: dict) -> ResultBase:
    """
        Verifica se o domínio da URL é semelhante a um domínio conhecido, indicando uma possível tentativa de typosquatting.
        - O typosquatting é uma técnica onde atacantes registram domínios semelhantes a domínios legítimos, com o objetivo de enganar os usuários e redirecioná-los para sites maliciosos.
        - A função extrai o domínio da URL e o compara com uma lista de domínios conhecidos, utilizando técnicas de detecção de similaridade para identificar possíveis casos de typosquatting.    
        - O resultado inclui o valor da detecção, uma versão normalizada do domínio e detalhes adicionais sobre a similaridade encontrada.

        Atributos:
            - structure (dict): Um dicionário contendo informações sobre a URL a ser analisada

        Retorna:
            - ResultBase: Um objeto contendo o resultado da análise, incluindo o valor da detecção, uma versão normalizada do domínio e detalhes adicionais sobre a similaridade encontrada. 

        Exemplo:
            structure = {
                "url": "http://gооgle.com"
            }
            result = typosquatting(structure)
            print(result.value)  # True
            print(result.normalized)  # "google"
            print(result.details)  # {"similarity_score": 0.86, "matched_domain": "google"}
    """

    url = structure.get("url", "")
    if not url:
        return ResultBase(
            value = 0.0,
            normalized = 0.0,
            details = {
                "similarity_score": 0.0,
                "matched_domain": None
            }
        )

    domain = extract_domain(url)
    result = detect(domain, BY_LEN)

    return ResultBase(
        value = result.value,
        normalized = result.normalized,
        details = result.details
    )   
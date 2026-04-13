from urllib.parse import urlparse, parse_qs
from tldextract import extract

def extract_structure(url: str):
    """
        Extrai características estruturais de uma URL para análise.

        A função recebe uma URL e retorna um dicionário com informações
        detalhadas sobre sua composição, incluindo esquema, domínio,
        porta, caminho, parâmetros de consulta e fragmento, bem como
        métricas derivadas como comprimento do URL, comprimento do domínio,
        número de subdomínios, número de hífens e contagem de parâmetros
        de consulta.

        Essas características são úteis para:
            - análise de URLs maliciosas
            - detecção de phishing e typosquatting
            - cálculo de métricas de complexidade ou entropia de URLs
            - uso em algoritmos de aprendizado de máquina que classificam URLs

        Args:
            url (str): URL que será analisada.

        Returns:
            dict: Dicionário contendo as características extraídas:
                - "url": URL original
                - "scheme": esquema (http, https)
                - "hostname": domínio principal
                - "port": porta (se especificada)
                - "path": caminho da URL
                - "params": parâmetros de rota (URL params)
                - "query": string de consulta
                - "fragment": fragmento da URL (#)
                - "url_length": comprimento total da URL
                - "domain_length": comprimento do domínio
                - "path_length": comprimento do caminho
                - "subdomain_count": quantidade de subdomínios
                - "hyphen_count": quantidade de hífens no domínio
                - "query_param_count": quantidade de parâmetros na query
                - "query_length": comprimento da string de query

            Retorna None caso a URL não possua um domínio válido.

        Exemplo:
            ```
                >>> extract_features("https://www.exemplo.com/path?arg=1#frag")
                {
                    "url": "https://www.exemplo.com/path?arg=1#frag",
                    "scheme": "https",
                    "hostname": "www.exemplo.com",
                    "port": None,
                    "path": "/path",
                    "params": "",
                    "query": "arg=1",
                    "fragment": "frag",
                    "url_length": 35,
                    "domain_length": 15,
                    "path_length": 5,
                    "subdomain_count": 2,
                    "hyphen_count": 0,
                    "query_param_count": 1,
                    "query_length": 5
                }
            ```
    """
    
    if not url:
        return None

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    ext = extract(url)

    hostname = parsed.hostname
    registered_domain = f"{ext.domain}.{ext.suffix}"

    if not hostname:
        return None

    query_params = parse_qs(parsed.query)
    subs = [s for s in ext.subdomain.split(".") if s and s.lower() != "www"] if ext.subdomain else []
    subdomain_count = len(subs)

    return {
        "url": url,
        "scheme": parsed.scheme,
        "hostname": hostname,
        "registered_domain": registered_domain,
        "subdomain": subs,
        "port": parsed.port,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "url_length": len(url),
        "domain_length": len(registered_domain),
        "path_length": len(parsed.path),
        "subdomain_count": subdomain_count,
        "hyphen_count": hostname.count("-"),
        "equal_count": hostname.count("="),
        "query_param_count": len(query_params),
        "query_length": len(parsed.query)
    }   
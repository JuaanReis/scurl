import tldextract
from core.network.config_net import client

_RDAP_SERVERS: dict[str, str] = {
    "com":  "https://rdap.verisign.com/com/v1/domain/",
    "net":  "https://rdap.verisign.com/net/v1/domain/",
    "org":  "https://rdap.publicinterestregistry.org/rdap/domain/",
    "io":   "https://rdap.nic.io/domain/",
    "br":   "https://rdap.registro.br/domain/",
    "gov":  "https://rdap.arin.net/registry/domain/",
    "edu":  "https://rdap.arin.net/registry/domain/",
    "info": "https://rdap.afilias.info/rdap/info/domain/",
    "biz":  "https://rdap.nic.biz/domain/",
    "co":   "https://rdap.nic.co/domain/",
    "us":   "https://rdap.arin.net/registry/domain/",
    "uk":   "https://rdap.nominet.uk/uk/domain/",
    "de":   "https://rdap.denic.de/domain/",
    "fr":   "https://rdap.nic.fr/domain/",
    "host": "https://rdap.centralnic.com/host/domain/"
}

_RDAP_FALLBACK = "https://rdap.org/domain/"

def resolve_rdap_url(hostname: str) -> str:
    extracted = tldextract.extract(hostname)
    registered = f"{extracted.domain}.{extracted.suffix}"
    tld = extracted.suffix.lower()
    base = _RDAP_SERVERS.get(tld, _RDAP_FALLBACK)
    return f"{base}{registered}"

def fetch_rdap(hostname: str) -> dict | None:
    if not hostname:
        return None
    try:
        url = resolve_rdap_url(hostname)
        response = client.get(url)
        response.raise_for_status()
        data = response.json()
        if "errorCode" in data:
            return None
        return data
    except Exception as e:
        return None
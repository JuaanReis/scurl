from datetime import datetime, timezone
from core.network.config_net import clients
import tldextract
from core.math.exponential_decay import domain_age_score
from core.models.result_base import ResultBase

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
}

_RDAP_FALLBACK = "https://rdap.org/domain/"

_client = clients[0]

def domain_age(structure: dict) -> ResultBase:
    url = structure.get("hostname", "")

    if not url:
        return ResultBase(
            value=None,
            normalized=0.5,
            weight=0.0,
            details={
                "error": "No URL provided"
            }
        )

    try:
        rdap_url = _resolve_rdap_url(url)
        response = _client.get(rdap_url)
        response.raise_for_status()
        data = response.json()

        creation = _extract_creation_date(data)

        if creation is None:
            return ResultBase(
                value=None,
                normalized=None,
                weight=0.0,
                details={
                    "error": "Creation date not available"
                }
            )

        now = datetime.now(timezone.utc)
        age = now - creation
        score = domain_age_score(age.days)

        return ResultBase(
            value=age.days,
            normalized=score if score > 0.1 else 0.0,
            weight=4.5,
            details={
                "creation_date": creation.isoformat(),
                "age_days": age.days
            }
        )

    except Exception as e:
        return ResultBase(
            value=None,
            normalized=None,
            weight=1.0,
            details={"error": "RDAP lookup failed"}
        )

def _resolve_rdap_url(hostname: str) -> str:
    extracted = tldextract.extract(hostname)
    registered = f"{extracted.domain}.{extracted.suffix}"
    tld = extracted.suffix.lower()
    base = _RDAP_SERVERS.get(tld, _RDAP_FALLBACK)
    return f"{base}{registered}"

def _extract_creation_date(data: dict) -> datetime | None:
    for event in data.get("events", []):
        if event.get("eventAction") == "registration":
            raw = event.get("eventDate")
            if raw:
                return _parse_rdap_date(raw)
    return None

def _parse_rdap_date(raw: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None
import re
import socket
from urllib.parse import urlparse
from ipwhois import IPWhois
from core.models.result_base import ResultBase
from .response import HTMLParser
from ..check.normalize_domain import normalize_domain

TRUSTED_DOMAINS = {normalize_domain(d) for d in {
    "cdn.jsdelivr.net", "cdnjs.cloudflare.com", "ajax.googleapis.com",
    "code.jquery.com", "stackpath.bootstrapcdn.com", "unpkg.com",
    "fonts.googleapis.com", "fonts.gstatic.com",
    "static.cloudflareinsights.com", "www.googletagmanager.com",
    "googletagmanager.com", "www.google-analytics.com", "google-analytics.com",
    "www.google.com", "recaptcha.google.com", "google.com",
    "cloudfront.net",
}}

RESOURCE_CATEGORY = {
    "cdn":       {normalize_domain(d) for d in {
                    "cdn.jsdelivr.net", "cdnjs.cloudflare.com", "unpkg.com",
                    "stackpath.bootstrapcdn.com", "code.jquery.com"}},
    "analytics": {normalize_domain(d) for d in {
                    "www.googletagmanager.com", "googletagmanager.com",
                    "www.google-analytics.com", "google-analytics.com",
                    "static.cloudflareinsights.com"}},
    "font":      {normalize_domain(d) for d in {
                    "fonts.googleapis.com", "fonts.gstatic.com"}},
    "captcha":   {normalize_domain(d) for d in {
                    "www.google.com", "recaptcha.google.com", "google.com"}},
}

HARVEST_PATTERNS = [
    re.compile(r'fetch\s*\('),
    re.compile(r'XMLHttpRequest'),
    re.compile(r'\.open\s*\(\s*["\']POST'),
    re.compile(r'form\.submit\s*\('),
    re.compile(r'addEventListener\s*\(\s*["\']submit'),
    re.compile(r'FormData\s*\('),
]

def _categorize(domain: str) -> str:
    norm = normalize_domain(domain)
    for category, domains in RESOURCE_CATEGORY.items():
        if any(norm.endswith(d) for d in domains):
            return category
    return "unknown"

_asn_cache: dict[str, str | None] = {}

def _get_asn(domain: str) -> str | None:
    norm = normalize_domain(domain)
    if norm in _asn_cache:
        return _asn_cache[norm]
    try:
        ip = socket.gethostbyname(norm)
        asn = IPWhois(ip).lookup_rdap(depth=1).get("asn")
        _asn_cache[norm] = asn
        return asn
    except Exception:
        _asn_cache[norm] = None
        return None

def _detect_harvest(tree: HTMLParser, external_domains: set[str]) -> list[str]:
    findings = []
    for script in tree.css("script:not([src])"):
        text = script.text() or ""
        has_harvest = any(p.search(text) for p in HARVEST_PATTERNS)
        if not has_harvest:
            continue
        for domain in external_domains:
            if normalize_domain(domain) in text:
                findings.append(domain)
    return findings

def external_script(tree: HTMLParser | None, structure: dict) -> ResultBase:
    if tree is None:
        return ResultBase(
            value=0,
            normalized=None,
            weight=3.0,
            details={"error": "Não foi possível analisar o HTML da resposta."}
        )

    original_domain = normalize_domain(structure.get("hostname", ""))
    page_asn = _get_asn(original_domain)

    scripts = tree.css('script[src]')
    external_scripts   = []
    suspicious_scripts = []
    domain_categories  = {}
    external_domains   = set()

    for script in scripts:
        src = script.attributes.get('src', '')
        if not src:
            continue
        parsed = urlparse(src)
        script_domain = normalize_domain(parsed.netloc)
        if not script_domain or script_domain == original_domain:
            continue

        external_scripts.append(src)
        external_domains.add(script_domain)

        category = _categorize(script_domain)
        domain_categories[script_domain] = category

        if any(script_domain.endswith(t) for t in TRUSTED_DOMAINS):
            continue

        script_asn = _get_asn(script_domain)
        if page_asn and script_asn and page_asn == script_asn:
            domain_categories[script_domain] = "same_infra"
            continue

        suspicious_scripts.append(src)

    unique_external = len(external_domains)
    harvest_domains = _detect_harvest(tree, external_domains)

    has_suspicious = len(suspicious_scripts) > 0
    has_harvest    = len(harvest_domains) > 0

    if has_harvest:
        score = 1.0
    elif has_suspicious:
        ratio = min(len(suspicious_scripts) / max(len(external_scripts), 1), 1.0)
        score = 0.5 + 0.5 * ratio
    else:
        score = 0.0

    return ResultBase(
        value=score,
        normalized=score if score > 0 else None,
        weight=3.0,
        details={
            "has_suspicious_external_script": has_suspicious,
            "external_script_count": len(external_scripts),
            "suspicious_script_count": len(suspicious_scripts),
            "unique_external_domains": unique_external,
            "domain_categories": domain_categories,
            "suspicious_scripts": suspicious_scripts,
            "harvest_detected": has_harvest,
            "harvest_domains": harvest_domains,
        }
    )
import re
from urllib.parse import urlparse
from core.models.result_base import ResultBase
from .response import HTMLParser
from ..check.normalize_domain import normalize_domain

JS_ASSIGNMENT_PATTERN = re.compile(
    r'(?:window\.location|window\.location\.href|location\.replace\s*\()\s*=\s*["\']([^"\']+)["\']'
)

def redirect_check(tree: HTMLParser | None, structure: dict) -> ResultBase:
    if tree is None:
        return ResultBase(
            value=0,
            normalized=None,
            weight=3.0,
            details={"error": "Não foi possível analisar o HTML da resposta."}
        )

    original_domain = structure.get("hostname", "")
    redirects = []

    for meta in tree.css('meta[http-equiv="refresh"]'):
        content = meta.attributes.get("content", "")
        if "url=" in content.lower():
            url_part = content.lower().split("url=")[-1].strip()
            parsed = urlparse(url_part)
            if parsed.netloc and normalize_domain(parsed.netloc) != normalize_domain(original_domain):
                redirects.append({"type": "meta_refresh", "target": url_part})

    for script in tree.css("script"):
        text = script.text() or ""
        for match in JS_ASSIGNMENT_PATTERN.finditer(text):
            target = match.group(1)
            parsed = urlparse(target)
            if parsed.netloc and normalize_domain(parsed.netloc) != normalize_domain(original_domain):
                redirects.append({"type": "js_redirect", "target": target})

    has_redirect = len(redirects) > 0

    return ResultBase(
        value=1.0 if has_redirect else 0.0,
        normalized=1.0 if has_redirect else None,
        weight=3.0,
        details={
            "has_external_redirect": has_redirect,
            "redirect_count": len(redirects),
            "redirects": redirects
        }
    )
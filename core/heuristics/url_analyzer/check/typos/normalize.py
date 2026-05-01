import unicodedata

HOMOGLYPHS = {
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "ӏ": "l",
}

def normalize_domain(domain: str) -> str:
    domain = unicodedata.normalize("NFKC", domain)

    for k, v in HOMOGLYPHS.items():
        domain = domain.replace(k, v)

    return domain.lower()
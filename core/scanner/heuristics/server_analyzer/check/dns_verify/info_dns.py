import dns.resolver

def get_dns_info(hostname: str) -> dict:
    result = {}

    hostname = hostname.removeprefix("www.").strip().lower()

    try:
        answers = dns.resolver.resolve(hostname, 'A')
        result["ips"] = [r.address for r in answers]
        result["ttl"] = answers.rrset.ttl
    except Exception:
        result["ips"] = []
        result["ttl"] = None

    try:
        dns.resolver.resolve(hostname, 'MX')
        result["has_mx"] = True
    except Exception:
        result["has_mx"] = False

    try:
        txt_answers = dns.resolver.resolve(hostname, 'TXT')
        result["txt"] = [str(r) for r in txt_answers]
    except Exception:
        result["txt"] = []

    return result

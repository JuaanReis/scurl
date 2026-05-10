from datetime import datetime, timezone


def infer(data: dict) -> dict:
    headers:     dict = data.get("raw", {}).get("headers", {})
    target:      dict = data.get("target", {})
    meta:        dict = data.get("meta", {})
    dns_details: dict = _get_heuristic_details(data, "dns_verify")

    server_header = headers.get("server", "").upper()
    alt_svc       = headers.get("alt-svc", "")
    csp           = headers.get("content-security-policy", "")
    encoding      = headers.get("content-encoding", "none")
    hsts          = headers.get("strict-transport-security", "")
    xss           = headers.get("x-xss-protection", "")
    permissions   = headers.get("permissions-policy", "")

    is_google    = any(k in server_header for k in ["ESF", "GSE", "GFE", "GOOGLE"])
    http3        = "h3=" in alt_svc
    cdn_likely   = is_google or "cloudflare" in server_header.lower()
    edge_detected = is_google or http3
    trusted_types = "require-trusted-types-for" in csp
    xss_enabled   = xss != "0" and xss != ""
    load_balanced = dns_details.get("ip_count", 1) > 1 or dns_details.get("ttl", 999) < 120

    scan_id_full   = meta.get("scan_id", "?")
    scan_id_short  = (
        f"{scan_id_full[:8]}-{scan_id_full[8:14]}"
        if len(scan_id_full) >= 14 else scan_id_full
    )

    url_hash_full  = meta.get("url_hash", "?")
    url_hash_short = url_hash_full[:18] + "..." if len(url_hash_full) > 18 else url_hash_full

    ts_raw = meta.get("timestamp", "")
    try:
        ts = datetime.fromisoformat(ts_raw).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        ts = ts_raw

    return {
        "is_google":      is_google,
        "http3":          http3,
        "cdn_likely":     cdn_likely,
        "edge_detected":  edge_detected,
        "trusted_types":  trusted_types,
        "xss_enabled":    xss_enabled,
        "load_balanced":  load_balanced,
        "scan_id_short":  scan_id_short,
        "url_hash_short": url_hash_short,
        "timestamp":      ts,
        "encoding":       encoding,
        "hsts":           hsts,
        "csp":            csp,
        "permissions":    permissions,
    }

def _get_heuristic_details(data: dict, name: str) -> dict:
    for h in data.get("heuristics", []):
        if h.get("name") == name:
            return h.get("details", {})
    return {}
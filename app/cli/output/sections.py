from .formatter import row, section, enabled, yes_no, present, likely, risk_label

def print_target(target: dict, inferred: dict):
    section("Target")
    print(row("URL", target.get("original_url", target.get("url", "?"))))
    print(row("Host",       target.get("hostname", "?")))
    print(row("Registered", target.get("registered_domain", "?")))
    print(row("Scheme",     target.get("scheme", "?").upper()))
    print(row("Subdomains", str(target.get("subdomain_count", 0))))
    print(row("HTTPS",      enabled(target.get("is_https"))))

def print_network(network: dict, inferred: dict):
    section("Network")
    print(row("Status",        f"{network.get('status_code', '?')} OK"))
    print(row("Response Time", f"{float(network.get('response_time_s', 0)):.3f}s"))
    print(row("Payload Size",  f"{network.get('size_kb', 0):.1f} KB"))
    print(row("Compression",   inferred["encoding"].upper()))
    print(row("Redirects",     str(network.get("redirects", 0))))
    print(row("HTTP3",         enabled(inferred["http3"])))

def print_redirect_chain(raw: dict):
    chain = raw.get("redirect_chain", [])
    redirects = raw.get("redirects", 0)
    if redirects > 0:
        section("Redirect Chain")
        for step in chain:
            print(f"[{step['status']}] {step['url']}")
            if step.get("location"):
                print(f"  └─→ {step['location']}")

def print_infrastructure(headers: dict, inferred: dict):
    section("Infrastructure")
    print(row("Server",       headers.get("server", "UNKNOWN")))
    print(row("providers",     "Google" if inferred["is_google"] else "Unknown"))
    print(row("CDN",          "Likely" if inferred["cdn_likely"] else "Not Detected"))
    print(row("TLS",          "ENABLED"))
    print(row("Edge Network", "DETECTED" if inferred["edge_detected"] else "NOT DETECTED"))

def print_security_posture(headers: dict, inferred: dict):
    xframe   = headers.get("x-frame-options",       "DISABLED")
    xcontent = headers.get("x-content-type-options", "DISABLED")

    section("Security Posture")
    print(row("HSTS",           enabled(inferred["hsts"])))
    print(row("CSP",            enabled(inferred["csp"])))
    print(row("Trusted Types",  enabled(inferred["trusted_types"])))
    print(row("X-Frame",        xframe))
    print(row("X-Content-Type", xcontent))
    print(row("XSS Protection", enabled(inferred["xss_enabled"])))

def print_tls(ssl_details: dict):
    section("TLS Analysis")
    print(row("Issuer",         ssl_details.get("issuer", "?")))
    print(row("Self Signed",    yes_no(ssl_details.get("self_signed", False))))
    print(row("Hostname Match", yes_no(ssl_details.get("hostname_valid", False))))
    print(row("SAN Count",      str(ssl_details.get("san_count", "?"))))
    print(row("Cert Age",       f"{ssl_details.get('age_days', '?')}d"))
    print(row("Validity",       f"{ssl_details.get('validity_days', '?')}d"))

def print_dns(dns_details: dict, inferred: dict):
    section("DNS Intelligence")
    print(row("MX Record",    present(dns_details.get("has_mx"))))
    print(row("TTL",          str(dns_details.get("ttl", "?"))))
    print(row("IPs",          str(len(dns_details.get("a", [])))))  # <-- aqui
    print(row("Load Balanced", likely(inferred["load_balanced"])))

def print_fingerprint(meta: dict, inferred: dict):
    section("Fingerprint")
    print(row("Scan ID",    inferred["scan_id_short"]))
    print(row("URL SHA256", inferred["url_hash_short"]))
    print(row("Threads",    str(meta.get("threads", "?"))))
    print(row("Timestamp",  inferred["timestamp"]))

def print_engine(meta: dict, stats: dict):
    skipped      = max(0, stats.get("rules_total", 0) - stats.get("rules_triggered", 0))
    trigger_rate = stats.get("trigger_rate", 0)

    section("Engine")
    print(row("Processors",   str(meta.get("threads", "?"))))
    print(row("Rules Loaded", str(stats.get("rules_total", 0))))
    print(row("Triggered",    str(stats.get("rules_triggered", 0))))
    print(row("Suppressed",   str(skipped)))
    print(row("Trigger Rate", f"{trigger_rate * 100:.1f}%"))

def print_heuristics(heuristics: list):
    if not heuristics:
        return

    section("Heuristics")
    values_fmt = [f"{h.get('value', 0):.2f}" for h in heuristics]
    col_mod    = max(len(h.get("category", "")) for h in heuristics)
    col_rule   = max(len(h.get("name", ""))     for h in heuristics)
    col_val    = max(len(v) for v in values_fmt)

    print(f"{'MODULE'.ljust(col_mod)}  {'RULE'.ljust(col_rule)}  {'VALUE'.rjust(col_val)}  WEIGHT  CONTRIB")
    for h, val in zip(heuristics, values_fmt):
        print(
            f"{h.get('category', '').ljust(col_mod).upper()}  "
            f"{h.get('name', '').ljust(col_rule)}  "
            f"{val.rjust(col_val)}    "
            f"{h.get('weight', 0):.1f}      "
            f"{h.get('contribution', 0):.1f}"
        )

def print_findings(heuristics: list):
    from .formatter import _c, C_OK, C_WARN
    positives = []
    warnings  = []

    warn_keywords = ["suspeito", "antigo", "renovação", "não convencional"]

    for h in heuristics:
        for reason in h.get("reasons", []):
            if any(k in reason.lower() for k in warn_keywords):
                warnings.append(reason)
            else:
                positives.append(reason)

    if not positives and not warnings:
        return

    section("Findings")
    for f in positives:
        print(f"{_c(C_OK, '[+]')} {f}")
    for f in warnings:
        print(f"{_c(C_WARN, '[!]')} {f}")

def print_insights(heuristics: list, insight: list, inferred: dict):
    derived = []
    if inferred["is_google"]:
        derived.append("Target pertence provavelmente à infraestrutura Google")
    if inferred["http3"]:
        derived.append("HTTP/3 detectado via alt-svc")
    if inferred["trusted_types"]:
        derived.append("Política Trusted Types presente")
    if inferred["permissions"]:
        derived.append("Headers indicam hardening de navegador")

    all_insights = derived + insight
    if not all_insights:
        return

    section("Insights")
    for msg in all_insights:
        print(f"* {msg}")

def print_risk_score(result: dict):
    from .formatter import _c, C_OK, C_WARN, C_DANGER
    score = float(result.get("score", 0))
    risk  = str(result.get("risk_level", "")).upper()

    bar_filled = int((score / 100) * 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    if score >= 70:
        color = C_DANGER
    elif score >= 40:
        color = C_WARN
    else:
        color = C_OK

    section("Risk Score")
    print(_c(color, f"{score:.2f} / 100.00"))
    print(_c(color, f"[{bar}] {risk}"))

def print_footer(meta: dict, start_time=None):
    if start_time is not None:
        from time import time
        print(f"\nScurl concluído em {time() - start_time:.2f}s")
    else:
        print(f"\nScurl concluído em {float(meta.get('scan_time_s', 0)):.2f}s")
    print("─" * 40)
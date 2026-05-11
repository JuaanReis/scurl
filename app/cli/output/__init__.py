from .infer import infer, _get_heuristic_details
from .assessment import print_assessment
from .sections import (
    print_target,
    print_network,
    print_redirect_chain,
    print_infrastructure,
    print_security_posture,
    print_tls,
    print_dns,
    print_fingerprint,
    print_engine,
    print_heuristics,
    print_findings,
    print_insights,
    print_risk_vectors,
    print_risk_score,
    print_footer,
)

def print_output(scan: dict, target: dict, verbose: bool = False):
    status = scan.get("status")
    if status == "error":
        err: dict = scan.get("error", {})
        print(f"FALHA {err.get('type')}: {err.get('message')}")
        return

    engine:      dict = scan.get("engine", {})
    meta:        dict = scan.get("meta", {})
    result:      dict = scan.get("result", {})
    stats:       dict = scan.get("stats", {})
    heuristics:  list = scan.get("heuristics", [])
    insight:     list = scan.get("insight", [])
    network:     dict = target.get("network", {})
    raw:         dict = target.get("raw", {})
    headers:     dict = raw.get("headers", {})
    ssl_details: dict = _get_heuristic_details(scan, "ssl_score")
    dns_details: dict = _get_heuristic_details(scan, "dns_score")
    inferred = infer(scan, target)

    print_target(target, inferred)
    print_network(network, raw, inferred)
    print_redirect_chain(raw)
    print_infrastructure(headers, inferred)
    print_security_posture(headers, inferred)
    print_tls(ssl_details)
    print_dns(dns_details, inferred)
    print_fingerprint(meta, inferred)
    print_engine(meta, stats)
    print_heuristics(heuristics)
    print_findings(heuristics)
    print_insights(heuristics, insight, inferred)
    print_risk_vectors(heuristics, headers, inferred, network)
    print_risk_score(result)
    print_assessment(result)
    print_footer(meta)
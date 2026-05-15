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
    print_risk_score,
    print_footer,
)

def print_output(scan: dict, target: dict, verbose: bool = False, time=None):
    status = scan.get("status")
    if status == "error":
        err: dict = scan.get("error", {})
        print(f"FALHA {err.get('type')}: {err.get('message')}")
        return

    http: dict = target.get("http", {})
    meta:        dict = scan.get("meta", {})
    dns:     dict = target.get("dns", {})
    result:      dict = scan.get("result", {})
    stats:       dict = scan.get("stats", {})
    heuristics:  list = scan.get("heuristics", [])
    insight:     list = scan.get("insight", [])
    identity: dict = target.get("identity", {})
    headers:  dict = http.get("security_headers", {})
    ssl_details: dict = _get_heuristic_details(scan, "ssl_score")
    inferred = infer(scan, target)

    print_target(identity, inferred)
    print_network(http, inferred)
    print_redirect_chain(http)
    print_infrastructure(headers, inferred)
    print_security_posture(headers, inferred)
    print_tls(ssl_details)
    print_dns(dns, inferred)
    print_fingerprint(meta, inferred)
    print_engine(meta, stats)
    print_heuristics(heuristics)
    print_findings(heuristics)
    print_insights(heuristics, insight, inferred)
    print_risk_score(result)
    print_assessment(result)
    print_footer(meta, time)
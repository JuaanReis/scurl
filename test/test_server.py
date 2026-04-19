from core.scanner.heuristics.server_analyzer.rules.server_rules import SSLVerifyRule, DNSVerifyRule, DomainAgeRule, NameServerDiversityRule, RDAPFieldIncompletenessRule
from core.scanner.heuristics.url_analyzer.url_structure import extract_structure
from core.scanner.score.sigmoid import sigmoid
from core.scanner.score.weighted_average import weighted_average
from time import time

def _run():
    url = input("[?] Digite uma URL: ")
    if not url:
        print("[!] URL não informada. Encerrando.")
        return
    start = time()

    structure = extract_structure(url) or {}
    rules = [SSLVerifyRule(), DomainAgeRule(), DNSVerifyRule(), NameServerDiversityRule(), RDAPFieldIncompletenessRule()]

    scores = []
    weights = []

    for rule in rules:
        result = rule.run(structure)
        scores.append(result.value)
        weights.append(result.weight)
        print(f"[+] {result.name} | Value: {result.value} | Weight: {result.weight} | Details: {result.details}" if result.value is not None or result.value == 0 else f"[!] {result.name} | Value: N/A | Weight: {result.weight} | Details: {result.details}")

    score = sigmoid(scores, weights)
    print(f"\n[+] Final Score (Sigmoid): {score:.2f}% de risco")
    print(f"[+] Final Score (Weighted Average): {weighted_average(scores, weights):.2f}% de risco")
    print(f"[+] Analise feita em {time() - start:.2f} segundos")

if __name__ == "__main__":
    _run()
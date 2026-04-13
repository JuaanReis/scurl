from time import time

start = time()
from core.engine.context_aply import apply_dependencies
from core.scanner.heuristics.url_analyzer.rules.character_rules import NumRatioRiskRule, MixEncodingRule, AtRiskRule, HyphenRiskRule, EqualRiskRule, XSSPatternRule
from core.scanner.heuristics.url_analyzer.rules.parts_rules import RandomPathRiskRule, QueryNoValueRule, QueryContainsURLRule, Base64SegmentRule, PathDepthRiskRule, FragmentRiskRule
from core.scanner.heuristics.url_analyzer.rules.domain_rules import IPInURLRule, SubdomainCountRule, RandomDomainRiskRule, RandomSubdomainRiskRule
from core.scanner.heuristics.server_analyzer.rules.server_rules import SSLVerifyRule, DNSVerifyRule, DomainAgeRule
from core.scanner.heuristics.response_analyzer.rules.response_rules import ExternalScriptRule, FaviconRule, FormActionRule, HiddenFieldsRule, ImageSrcRule, ParseHtmlResponseRule, PasswordInputRule, RedirectRule
from core.scanner.heuristics.url_analyzer.url_structure import extract_structure
from core.scanner.score.sigmoid import sigmoid
print(f"[+] Imports carregados em {time() - start:.2f} segundos\n")

# ── dependências entre rules ──────────────────────────────────────────────────
#
# Cada entrada define como o peso de uma rule é ajustado com base
# no resultado de outra. Formato:
#
# "rule_alvo": [
#     {
#         "depends_on": "rule_fonte",
#         "condition": fn(valor_da_fonte) -> bool,
#         "action": "skip" | "reduce" | "increase",
#         "factor": float,   # multiplicador do peso (só pra reduce/increase)
#         "reason": str,
#     }
# ]





def _run_engine():
    url = input("[?] Digite uma URL: ")
    print()
    if not url:
        print("[!] URL não informada. Encerrando.")
        return

    start = time()

    structure = extract_structure(url) or {}
    body_result = ParseHtmlResponseRule().run(structure)
    structure['html_parser'] = body_result.response

    rules = [
        SSLVerifyRule(), DomainAgeRule(), DNSVerifyRule(),
        NumRatioRiskRule(), MixEncodingRule(), AtRiskRule(), HyphenRiskRule(), EqualRiskRule(), XSSPatternRule(),
        RandomPathRiskRule(), QueryNoValueRule(), QueryContainsURLRule(), Base64SegmentRule(), PathDepthRiskRule(), FragmentRiskRule(),
        IPInURLRule(), SubdomainCountRule(), RandomDomainRiskRule(), RandomSubdomainRiskRule(),
        ExternalScriptRule(), FaviconRule(), ImageSrcRule(),
        RedirectRule(), HiddenFieldsRule(), PasswordInputRule(), FormActionRule()
    ]

    scores = []
    weights = []
    results_map: dict[str, float | None] = {}
    raw_results = []

    # primeira passagem — coleta todos os resultados brutos
    for rule in rules:
        result = rule.run(structure)
        raw_results.append(result)
        results_map[result.name] = result.value

    # segunda passagem — aplica dependências e imprime
    for result in raw_results:
        adj_value, adj_weight, reasons = apply_dependencies(
            result.name, result.value, result.weight, results_map
        )

        scores.append(adj_value)
        weights.append(adj_weight)

        prefix = "[+]" if adj_value is not None else "[-]"
        print(f"{prefix} {result.name} | Value: {adj_value} | Weight: {adj_weight:.2f} | Category:  | Details: {result.details}")
        for r in reasons:
            print(f"    ~ {r}")

    print(f"\n[+] Final Score (Sigmoid): {sigmoid(scores, weights):.2f}% de risco")
    print(f"[+] Analise feita em {time() - start:.2f} segundos")


if __name__ == "__main__":
    _run_engine()
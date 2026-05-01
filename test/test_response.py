from core.heuristics.response_analyzer.rules.response_rules import (
    ParseHtmlResponseRule,
    ExternalScriptRule, FaviconRule, IframeRule, ImageSrcRule,
    RedirectRule, HiddenFieldsRule, PasswordInputRule, FormActionRule
)
from core.heuristics.url_analyzer.url_structure import extract_structure
from core.scanner.score.sigmoid import sigmoid

def _run_engine():
    url = input("[?] Digite uma URL: ")
    if not url:
        print("[!] URL não informada. Encerrando.")
        return

    structure = extract_structure(url) or {}

    # Roda a requisição uma vez e injeta no context
    body_rule = ParseHtmlResponseRule()
    body_result = body_rule.run(structure)
    structure['html_parser'] = body_result.response  # None se falhou

    rules = [
        ExternalScriptRule(), FaviconRule(), IframeRule(), ImageSrcRule(),
        RedirectRule(), HiddenFieldsRule(), PasswordInputRule(), FormActionRule()
    ]

    scores, weights = [], []

    for rule in rules:
        result = rule.run(structure)
        scores.append(result.value)
        weights.append(result.weight)
        print(f"[+] {result.name} | Value: {result.value} | Weight: {result.weight} | Details: {result.details}" if result.value != None else f"[!] {result.name} | Value: N/A | Weight: {result.weight} | Details: {result.details}")

    score = sigmoid(scores, weights)
    print(f"\n[+] Final Score (Sigmoid): {score:.2f}% de risco")

if __name__ == "__main__":
    _run_engine()
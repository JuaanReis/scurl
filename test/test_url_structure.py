from core.scanner.heuristics.url_analyzer.rules.character_rules import NumRatioRiskRule, MixEncodingRule, AtRiskRule, HyphenRiskRule, EqualRiskRule, XSSPatternRule
from core.scanner.heuristics.url_analyzer.rules.parts_rules import RandomPathRiskRule, QueryNoValueRule, QueryContainsURLRule, Base64SegmentRule, PathDepthRiskRule, FragmentRiskRule
from core.scanner.heuristics.url_analyzer.rules.domain_rules import IPInURLRule, SubdomainCountRule, RandomDomainRiskRule, RandomSubdomainRiskRule
from core.scanner.heuristics.url_analyzer.url_structure import extract_structure
from core.scanner.score.sigmoid import sigmoid
from core.scanner.score.weighted_average import weighted_average
from time import time

def _run():
    try:
        url = input("[?] digite uma URL: ")
        if not url or url.strip() == "":
            print("Nenhuma URL fornecida. Encerrando o programa.")
            return
        
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada de URL não fornecida. Encerrando o programa.")
        return
    
    start = time()

    extructure = extract_structure(url) or {} # Garantir que extructure seja um dicionário mesmo que a extração falhe

    rules = [
        NumRatioRiskRule(),
        MixEncodingRule(),
        AtRiskRule(),
        HyphenRiskRule(),
        EqualRiskRule(),
        XSSPatternRule(),
        RandomPathRiskRule(),
        QueryNoValueRule(),
        QueryContainsURLRule(),
        Base64SegmentRule(),
        PathDepthRiskRule(),
        FragmentRiskRule(),
        IPInURLRule(),
        SubdomainCountRule(),
        RandomDomainRiskRule(),
        RandomSubdomainRiskRule(),
    ]

    score = []
    weight = []

    for rule in rules:
        result = rule.run(extructure)
        score.append(result.value)
        weight.append(result.weight)
        
        print(f"[+] {result.name} | Value: {result.value} | Weight: {result.weight} | Details: {result.details}" if result.value != None else f"[!] {result.name} | Value: N/A | Weight: {result.weight} | Details: {result.details}")
    print(f"\n[+] Score final (Sigmoid): {sigmoid(score, weight):.2f}% de risco.")
    print(f"[+] Score final (Weighted Average): {weighted_average(score, weight):.2f}% de risco.")
    print(f"\n[+] {time() - start:.2f} segundos de análise completa.")

if __name__ == "__main__":
    _run()
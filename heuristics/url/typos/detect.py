from .normalize import normalize_domain
from core.math.levenshtein import levenshtein
from core.math.shannon_entropy import shannon_entropy
from core.models.result_base import ResultBase
from core.math.value_normalizator import minmax

def detect(domain: str, by_len: dict, threshold: float = 0.35, max_dist: int = 2) -> ResultBase:
    domain = normalize_domain(domain)

    if not domain:
        return ResultBase(result=None, risk=False)

    if domain.isdigit():
        return ResultBase(result=None, risk=False)

    if len(domain) < 4:
        return ResultBase(result=None, risk=False)

    domain_len = len(domain)

    best_distance = float("inf")
    best_match = None

    for l in range(domain_len - 2, domain_len + 3):

        for legit in by_len.get(l, ()):

            if not legit:
                continue

            if legit[0] != domain[0]:
                continue
            
            length_diff = abs(len(legit) - domain_len)
            if length_diff > max_dist:
                continue

            if length_diff > max_dist:
                continue

            d = levenshtein(domain, legit)

            if d > max_dist:
                continue

            if d < best_distance:
                best_distance = d
                best_match = legit

                if d == 0:
                    break

        if best_distance == 0:
            break

    if best_match is None:
        return ResultBase(result=None, risk=False)

    max_len = max(domain_len, len(best_match))
    similarity = 1 - (best_distance / max_len)

    entropy = shannon_entropy(domain)
    entropy_norm = min(entropy / 4.7, 1.0)

    if similarity < 0.85:
        risk_score = (1 - similarity) * 0.8 + entropy_norm * 0.2
    else:
        risk_score = 0.0
    
    normalized = minmax(risk_score, 0.0, 1.0)

    return ResultBase(
        value = risk_score,
        normalized = normalized if normalized > 0 else None,
        details = {
            "domain": domain,
            "best_match": best_match,
            "distance": best_distance,
            "similarity": similarity,
            "entropy": entropy,
            "entropy_norm": entropy_norm
        }
    )
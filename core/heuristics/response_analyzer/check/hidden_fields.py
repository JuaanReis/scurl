from core.models.result_base import ResultBase
from .response import HTMLParser

HIDDEN_FIELD_THRESHOLD = 5
 
def hidden_fields_check(tree: HTMLParser | None, structure: dict) -> ResultBase:
    if tree is None:
        return ResultBase(
            value=0,
            normalized=None,
            weight=2.0,
            details={"error": "Não foi possível analisar o HTML da resposta."}
        )
 
    hidden_inputs = tree.css('input[type="hidden"]')
    count = len(hidden_inputs)
    normalized = min(count / HIDDEN_FIELD_THRESHOLD, 1.0) if count > 0 else None
 
    return ResultBase(
        value=float(count),
        normalized=normalized,
        weight=2.0,
        details={
            "hidden_field_count": count,
            "threshold": HIDDEN_FIELD_THRESHOLD,
            "above_threshold": count >= HIDDEN_FIELD_THRESHOLD
        }
    )
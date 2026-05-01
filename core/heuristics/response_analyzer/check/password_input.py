from core.models.result_base import ResultBase
from .response import HTMLParser

def password_input_check(tree: HTMLParser | None, structure: dict) -> ResultBase:
    if tree is None:
        return ResultBase(
            value=0,
            normalized=None,
            weight=3.0,
            details={"error": "Não foi possível analisar o HTML da resposta."}
        )
 
    password_inputs = tree.css('input[type="password"]')
    has_password = len(password_inputs) > 0
 
    return ResultBase(
        value=1.0 if has_password else 0.0,
        normalized=1.0 if has_password else None,
        weight=4.0,
        details={
            "has_password_input": has_password,
            "password_input_count": len(password_inputs)
        }
    )
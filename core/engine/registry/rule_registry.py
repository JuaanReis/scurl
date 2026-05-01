from typing import Type

_REGISTRY: list[Type] = []

def register(cls: Type) -> Type:
    """
    Decorator que registra uma ScanRule automaticamente.

    Uso:
        @register
        class SSLVerifyRule(ScanRule):
            ...
    """
    
    if cls not in _REGISTRY:
        _REGISTRY.append(cls)
    return cls

def get_rules() -> list[Type]:
    return list(_REGISTRY)
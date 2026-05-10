from dataclasses import dataclass
from typing import Callable

@dataclass
class RuleEntry:
    fn: Callable
    name: str
    category: str
    severity: str
    weight: float
    tags: list[str]

_REGISTRY: list[RuleEntry] = []

def register(name: str, category: str, severity: str, weight: float, tags: list[str] = []):
    def decorator(fn: Callable) -> Callable:
        _REGISTRY.append(RuleEntry(
            fn=fn,
            name=name,
            category=category,
            severity=severity,
            weight=weight,
            tags=tags,
        ))
        return fn
    return decorator

def get_rules() -> list[RuleEntry]:
    return list(_REGISTRY)
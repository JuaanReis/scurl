from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class RuleEntry:
    fn: Callable
    name: str
    category: str
    severity: str
    weight: float
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

_REGISTRY: list[RuleEntry] = []

def register(name: str, category: str, severity: str, weight: float, tags: list[str] = [], **kwargs):
    def decorator(fn: Callable) -> Callable:
        _REGISTRY.append(RuleEntry(
            fn=fn,
            name=name,
            category=category,
            severity=severity,
            weight=weight,
            tags=tags,
            extra=kwargs,
        ))
        return fn
    return decorator

def get_rules() -> list[RuleEntry]:
    return list(_REGISTRY)
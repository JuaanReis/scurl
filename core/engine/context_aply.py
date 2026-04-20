from ..engine.dependencies import DEPENDENCIES


def apply_dependencies(name: str, value: float | None, weight: float, results_map: dict[str, float | None]) -> tuple[float | None, float, list[str]]:
    reasons: list[str] = []

    for dep in DEPENDENCIES.get(name, []):
        source_value = results_map.get(dep["depends_on"])

        try:
            triggered = dep["condition"](source_value)
        except Exception:
            continue

        if not triggered:
            continue

        action = dep["action"]

        if action == "skip":
            reasons.append(dep["reason"])
            return None, weight, reasons

        if action in ("reduce", "increase") and value is not None and value > 0:
            weight *= dep["factor"]
            reasons.append(dep["reason"])

    return value, weight, reasons
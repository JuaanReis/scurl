from ..engine.dependencies import DEPENDENCIES

def apply_dependencies(name: str, value: float | None, weight: float, results_map: dict[str, float | None]) -> tuple[float | None, float, list[str]]:
    rules = DEPENDENCIES.get(name, [])
    reasons = []
    skip = False

    for dep in rules:
        source_value = results_map.get(dep["depends_on"])
        try:
            triggered = dep["condition"](source_value)
        except Exception:
            continue

        if not triggered:
            continue

        action = dep["action"]

        if action == "skip":
            skip = True
            reasons.append(dep["reason"])
            break

        elif action == "reduce":
            if value is not None and value > 0:
                weight *= dep["factor"]
                reasons.append(dep["reason"])

        elif action == "increase":
            if value is not None and value > 0:
                weight *= dep["factor"]
                reasons.append(dep["reason"])

    if skip:
        return None, weight, reasons
    
    return value, weight, reasons
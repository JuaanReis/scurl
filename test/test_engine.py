import core.heuristics
from core.models.scan_context import ScanContext
from core.engine.registry.rule_registry import get_rules
from core.engine.pipeline import (
    validate_target,
    collect_target_data,
    execute_rules,
)

def observe_results(url: str, timeout: float = 5, processors: int = 2, retries: int = 3):

    ctx = ScanContext(url)

    if error := validate_target(ctx):
        return error

    if error := collect_target_data(ctx, timeout, retries):
        return error

    rules = [rule() for rule in get_rules()]

    if error := execute_rules(ctx, rules, processors):
        return error

    for k, v in ctx.results_map.items():
        if v is None:
            status = "N/A"
        else:
            status = f"{v:.2f}"

        print(f"{k:25} -> {status}")

if __name__ == "__main__":
    url = input("[?] Digite uma URL: ")
    observe_results(str(url))
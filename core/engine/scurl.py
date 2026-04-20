import core.scanner.heuristics # Forces the importation of rules
from core.models.scan_context import ScanContext
from core.engine.rule_registry import get_rules
from core.engine.pipeline import (
    validate_target,
    collect_target_data,
    execute_rules,
    calculate_score,
    build_response,
    build_error_response,
)

def run_engine(url: str, processors: int = 2) -> dict:
    ctx = ScanContext(url)

    if error := validate_target(ctx):
        return error

    if error := collect_target_data(ctx):
        return error

    rules = [rule() for rule in get_rules()]
    
    if error := execute_rules(ctx, rules, processors):
        return build_error_response(ctx, **error["error"])

    calculate_score(ctx)
    return build_response(ctx, rules_total=len(rules))
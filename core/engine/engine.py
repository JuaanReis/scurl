import core.heuristics as heuristics
from providers.database.repository import find_by_hash, save_scan
from core.models.scan_context import ScanContext, TargetData
from core.heuristics.registry import get_rules
from pathlib import Path
from dotenv import load_dotenv
from core.engine.pipeline import (
    validate_target, collect_target_data,
    execute_rules, calculate_score,
    build_response, build_error_response,
    meta_attribute
)

load_dotenv(Path(__file__).parent.parent.parent / ".env")
def run_engine(url: str, k: int = 5, timeout: float = 5, processors: int = 2, retries: int = 3, use_cache: bool = False) -> tuple[dict, dict]:
    ctx = ScanContext(target=TargetData(url=url))

    if use_cache:
        cached = find_by_hash(ctx.meta.url_hash)
        if cached:
            return cached

    if error := validate_target(ctx):
        return error, {}

    if error := collect_target_data(ctx, timeout, retries):
        return error, {}

    rules = get_rules()

    if error := execute_rules(ctx, rules, processors):
        return build_error_response(ctx, **error["error"]), {}

    meta_attribute(ctx, processors)
    calculate_score(ctx, k)

    scan_result, target_data = build_response(ctx, rules_total=len(rules))
    save_scan(scan_result, target_data)

    return scan_result, target_data
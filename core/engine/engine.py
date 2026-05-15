import core.heuristics as heuristics
from core.models.scan_context import ScanContext, TargetData
from core.heuristics.registry import get_rules
from providers.database.cache import load_cache, persist_scan
from core.engine.pipeline import (
    validate_target, collect_target_data,
    execute_rules, calculate_score,
    build_response, build_error_response,
    meta_attribute
)

def run_engine(url: str, k: int = 5, timeout: float = 5, processors: int = 2, retries: int = 3, use_cache: bool = False) -> tuple[dict, dict]:
    ctx = ScanContext(target=TargetData(url=url))

    if use_cache:
        if cached := load_cache(ctx.meta.url_hash):
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
    persist_scan(scan_result, target_data)

    return scan_result, target_data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the engine with a target URL.")
    parser.add_argument("--url", help="The target URL to scan.")  
    parser.add_argument("--k", type=int, default=5, help="Number of top rules to return.")
    parser.add_argument("--timeout", type=float, default=5, help="Timeout for data collection.")
    parser.add_argument("--processors", type=int, default=2, help="Number of processors to use for parallel execution.")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries for data collection.")
    parser.add_argument("--use-cache", action="store_true", help="Use cached results if available.")
    args = parser.parse_args()

    result, target_data = run_engine(
        url=args.url,
        k=args.k,
        timeout=args.timeout,
        processors=args.processors,
        retries=args.retries,
        use_cache=args.use_cache
    )

    print("Scan Result:")
    print(result)
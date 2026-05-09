import heuristics # Força a importação das heuristicas
from core.models.scan_context import ScanContext
from heuristics.registry import get_rules
from core.engine.pipeline import (
    validate_target,
    collect_target_data,
    execute_rules, calculate_score,
    build_response,
    build_error_response,
    meta_attribute
)

def run_engine(url: str, k: int = 5, timeout: float = 5, processors: int = 2, retries: int = 3) -> dict:
    ctx = ScanContext(url)
    
    if error := validate_target(ctx):
        return error

    if error := collect_target_data(ctx, timeout, retries):
        return error

    rules = get_rules()
    
    if error := execute_rules(ctx, rules, processors):
        return build_error_response(ctx, **error["error"])

    meta_attribute(ctx, processors)
    calculate_score(ctx, k)
    
    return build_response(ctx, rules_total=len(rules))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the SCURL engine.")
    parser.add_argument("--url", help="The target URL to scan.")
    parser.add_argument("-k", type=int, default=5, help="Number of top rules to return.")
    parser.add_argument("--timeout", type=float, default=5, help="Timeout for HTTP requests.")
    parser.add_argument("--processors", type=int, default=2, help="Number of processors to use.")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries for HTTP requests.")

    args = parser.parse_args()
    
    result = run_engine(args.url, args.k, args.timeout, args.processors, args.retries)
    print(result)
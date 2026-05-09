import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
from core.models.scan_context import ScanContext
from core.models.scan_result import ScanResult
logger = logging.getLogger(__name__)

MAX_SCAN_SECONDS = 15

def execute_rules(ctx: ScanContext, rules: list, processors: int) -> dict | None:
    frozen = dict(ctx.structure)

    with ThreadPoolExecutor(max_workers=min(processors, 8)) as executor:
        future_map = {executor.submit(rule.fn, frozen): rule for rule in rules}

        try:
            for future in as_completed(future_map, timeout=MAX_SCAN_SECONDS):
                rule = future_map[future]
                data = future.result()

                if data is None:
                    logger.warning("Rule %s retornou None, ignorando", rule.name)
                    continue

                ctx.results.append(ScanResult(
                    name=rule.name,
                    value=data.normalized,
                    weight=rule.weight,
                    category=rule.category,
                    severity=rule.severity,
                    details=data.details,
                ))

        except FuturesTimeout:
            executor.shutdown(wait=False, cancel_futures=True)
            logger.error("Scan timeout para %s", ctx.url)
            return {
                "status": "error",
                "error": {
                    "type": "scan_timeout",
                    "message": "Scan excedeu o tempo limite"
                }
            }

    ctx.results_map = {r.name: r.value for r in ctx.results}
    return None
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
from core.models.scan_context import ScanContext
logger = logging.getLogger(__name__)

MAX_SCAN_SECONDS = 15

def execute_rules(ctx: ScanContext, rules: list, processors: int) -> dict | None:
    """
    Executa todas as rules em paralelo.
    Retorna dict de erro em caso de timeout, None se ok.
    """
    frozen = dict(ctx.structure) 

    with ThreadPoolExecutor(max_workers=min(processors, 8)) as executor:
        future_map = {executor.submit(rule.run, frozen): rule for rule in rules}

        try:
            for future in as_completed(future_map, timeout=MAX_SCAN_SECONDS):
                result = future.result()
                if result is None:
                    logger.warning(
                        "Rule %s retornou None, ignorando",
                        type(future_map[future]).__name__
                    )
                    continue
                ctx.results.append(result)

        except FuturesTimeout:
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
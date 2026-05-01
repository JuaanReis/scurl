from core.engine.pipeline.response_validator import response_validator
from core.models.scan_context import ScanContext
from core.engine.pipeline.get_structure import get_structure

def collect_target_data(ctx: ScanContext, timeout: float = 5, retries: int = 3) -> dict | None:
    structure, response = get_structure(ctx.url, timeout, retries)
    ctx.structure = structure
    ctx.response = response
    return response_validator(response, ctx.url, ctx.start)
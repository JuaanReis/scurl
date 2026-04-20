from core.models.scan_context import ScanContext
from core.engine.url_extract.get_structure import get_structure
from core.engine.url_validator import response_validator

def collect_target_data(ctx: ScanContext) -> dict | None:
    structure, response = get_structure(ctx.url)
    ctx.structure = structure
    ctx.response = response
    return response_validator.response_validator(response, ctx.url, ctx.start)
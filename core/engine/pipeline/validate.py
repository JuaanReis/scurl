from core.models.scan_context import ScanContext
from core.engine.pipeline import url_validator

def validate_target(ctx: ScanContext) -> dict | None:
    return url_validator.url_validator(ctx.url)
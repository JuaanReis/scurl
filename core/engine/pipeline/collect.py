from core.models.scan_context import ScanContext
from core.engine.pipeline.validate_response import response_validator
from core.engine.pipeline.target_structure import get_structure
from providers.http.connect import get_response
from providers.rdap.fetch_rdap import fetch_rdap
from core.parsers.html_parser import parse_html
from providers.safebrowsing.client import fetch_safe_browsing

def collect_target_data(ctx: ScanContext, timeout: float = 5, retries: int = 3) -> dict | None:
    structure = get_structure(ctx.target.url)
    ctx.target.structure = structure
    ctx.target.safe_browsing = fetch_safe_browsing(ctx.target.url)

    response = get_response(url=ctx.target.url, timeout=timeout, retries=retries)
    ctx.target.response = response
    ctx.target.size_kb = round(response.size / 1024, 2) if response else 0

    if response and response.body:
        content_type = response.headers.get("content-type", "")
        if "html" in content_type.lower():
            ctx.target.html = parse_html(response.body)

    ctx.target.rdap = fetch_rdap(structure.get("hostname", ""))

    return response_validator(response, ctx.target.url, ctx.meta.start)
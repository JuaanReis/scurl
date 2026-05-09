from core.models.scan_context import ScanContext
from core.engine.pipeline.response_validator import response_validator
from core.engine.pipeline.get_structure import get_structure
from parser.html_parser import parse_html_response
from providers.rdap.fetch_rdap import fetch_rdap

def collect_target_data(ctx: ScanContext, timeout: float = 5, retries: int = 3) -> dict | None:
    structure = get_structure(ctx.url)

    html_parser, structure, response = parse_html_response(structure, timeout, retries)
    structure["html_parser"] = html_parser
    structure["rdap"] = fetch_rdap(structure.get("hostname", ""))

    ctx.structure = structure
    ctx.response = response
    ctx.size = round(response.size / 1024, 2) if response else 0

    return response_validator(response, ctx.url, ctx.meta.start)
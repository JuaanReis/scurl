from core.models.http_result import HTTPResult
from core.scanner.heuristics.response_analyzer.rules.response_rules import ParseHtmlResponseRule
from core.scanner.heuristics.url_analyzer.url_structure import extract_structure
from core.network.fetch_rdap import fetch_rdap

def get_structure(url: str) -> tuple[dict, HTTPResult]:
    structure = extract_structure(url) or {}
    body_result = ParseHtmlResponseRule().run(structure)
    structure["html_parser"] = getattr(body_result, "html", None)
    structure["rdap"] = fetch_rdap(structure.get("hostname", ""))
    response = body_result.response
    return structure, response
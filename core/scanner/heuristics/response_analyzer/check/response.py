from core.models.http_result import HTTPResult
from core.network.get_request import get_response
from selectolax.parser import HTMLParser

def parse_html_response(structure: dict) -> tuple[HTMLParser | None, dict, HTTPResult | None]:

    url = structure.get("url", "")
    response = get_response(url)

    if response is None:
        return None, structure, None

    if not response.body:
        return None, structure, response

    content_type = response.headers.get("content-type", "")

    if "html" not in content_type.lower():
        return None, structure, response

    parser = HTMLParser(response.body)

    return parser, structure, response
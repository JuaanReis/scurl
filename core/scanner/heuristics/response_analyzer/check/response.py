from core.network.get_request import get_response
from selectolax.parser import HTMLParser

def parse_html_response(structure: dict) -> tuple[HTMLParser | None, dict]:
    response = get_response(structure.get("url", ""))

    if response is None or response.body is None:
        return None, structure
    
    content_type = response.headers.get("content-type", "")
    
    if "html" not in content_type:
        return None, structure

    parser = HTMLParser(response.body)
    return parser, structure
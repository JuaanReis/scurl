from core.models.http_result import HTTPResult
from providers.http.connect import get_response
from selectolax.parser import HTMLParser

def parse_html_response(structure: dict, timeout: float, retries: int =3) -> tuple[HTMLParser | None, dict, HTTPResult | None]:

    url = structure.get("url", "")
    if not url:
        return None, structure, None
    
    response = get_response(url=url, timeout=timeout, retries=retries)
 
    if response is None:
        return None, structure, None

    if not response.body:
        return None, structure, response

    content_type = response.headers.get("content-type", "")

    if "html" not in content_type.lower():
        return None, structure, response

    parser = HTMLParser(response.body)

    return parser, structure, response
import logging
from time import sleep
from .client import scan_client, HTTPStatusError, ConnectError, RequestError, Timeout
from core.models.http_result import HTTPResult

logger = logging.getLogger(__name__)

def extract_redirect_chain(response):
    chain = []

    for r in response.history:
        chain.append({
            "url": str(r.url),
            "status": r.status_code,
            "location": r.headers.get("location")
        })

    chain.append({
        "url": str(response.url),
        "status": response.status_code,
        "location": None
    })

    return chain

def _build_result(response) -> HTTPResult:
    headers = dict(response.headers)
    headers.pop("set-cookie", None)
    headers.pop("Set-Cookie", None)  # Remove os cookies para evitar exposição de informações sensíveis

    return HTTPResult(
        url=str(response.url),
        status=response.status_code,
        headers=headers,
        body=response.text,
        elapsed=response.elapsed.total_seconds(),
        size=len(response.content),
        redirects=len(response.history),
        redirect_chain=extract_redirect_chain(response)
    )

def get_response(url: str, retries: int = 3, delay: float = 0.6, timeout: float = 5) -> HTTPResult | None:
    for attempt in range(retries):
        try:
            response = scan_client.get(url, timeout=timeout)
            return _build_result(response)

        except HTTPStatusError as e:
            response = e.response

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                sleep(retry_after)
                continue

            return _build_result(response)

        except (ConnectError, RequestError) as e:
            logger.warning(
                "Tentativa %d/%d falhou para %s: %s",
                attempt + 1, retries, url, e
            )

            sleep(delay * (2 ** attempt))

    return None
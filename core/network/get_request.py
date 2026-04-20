import logging
from time import sleep
from .config_net import client, HTTPStatusError, ConnectError, RequestError
from core.models.http_result import HTTPResult

logger = logging.getLogger(__name__)

def _build_result(response) -> HTTPResult:
    return HTTPResult(
        url=str(response.url),
        status=response.status_code,
        headers=response.headers,
        body=response.text,
        elapsed=response.elapsed.total_seconds(),
        size=len(response.content),
        redirects=len(response.history),
    )

def get_response(url: str, retries: int = 3, delay: float = 0.6) -> HTTPResult | None:
    for attempt in range(retries):
        try:
            return _build_result(client.get(url))

        except HTTPStatusError as e:
            response = e.response
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                sleep(retry_after)
                continue
            return _build_result(response)

        except (ConnectError, RequestError, Exception) as e:
            logger.warning("Tentativa %d/%d falhou para %s: %s", attempt + 1, retries, url, e)
            sleep(delay * (2 ** attempt))

    return None
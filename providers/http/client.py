from httpx import Client, Timeout, Limits, HTTPStatusError, ConnectError, RequestError, Timeout
from __init__ import __version__

def _base_limits() -> Limits:
    return Limits(max_keepalive_connections=20, max_connections=50)

def make_scan_client() -> Client:
    return Client(
        http2=False,
        verify=False,
        follow_redirects=True,
        timeout=Timeout(timeout=6.0, connect=1.5, read=3.0),
        limits=_base_limits(),
        headers={
            "Accept-Encoding": "gzip, br",
            "User-Agent": f"SCURL/{__version__}",
        },
    )

scan_client: Client = make_scan_client()
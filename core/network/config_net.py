from httpx import Client, Timeout, Limits, HTTPStatusError, ConnectError, RequestError, Timeout
from __init__ import __version__

client = Client(
    http2=False,
    verify=False,
    follow_redirects=True,
    timeout=Timeout(timeout=6.0, connect=1.5, read=3.0),
    limits=Limits(max_keepalive_connections=10, max_connections=20),
    headers={
        "Accept-Encoding": "gzip, br",
        "User-Agent": f"SCURL/{__version__}"
    }
)
from httpx import Client, Limits, Timeout
from importlib.metadata import version
__version__ = version("scurl")

def _base_limits() -> Limits:
    return Limits(max_keepalive_connections=20, max_connections=50)

def make_rdap_client() -> Client:
    return Client(
        http2=False,
        verify=True,  
        follow_redirects=True,
        timeout=Timeout(connect=2.0, read=3.0, write=2.0, pool=1.0),
        limits=_base_limits(),
        headers={
            "User-Agent": f"SCURL/{__version__}",
        },
    )

rdap_client: Client = make_rdap_client()
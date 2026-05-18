from core.models.scan_context import ScanContext
import ipaddress
import socket
from urllib.parse import urlparse
from scurl import config
from importlib.metadata import version

__version__ = version("scurl")

BLOCKED_RANGES = [
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("0.0.0.0/8"),
]


def _is_blocked_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if ip.is_private or ip.is_loopback or ip.is_link_local:
        return True
    return any(ip in r for r in BLOCKED_RANGES)

def _error_response(url: str | None, error_type: str, message: str) -> dict:
    return {
        "status": "error",
        "meta": {"url": url, "scan_time_s": 0, "version": __version__},
        "error": {"type": error_type, "message": message},
    }

def _is_private_or_local(url: str) -> str | None:
    try:
        host = urlparse(url).hostname
        if not host:
            return "error"

        if host in ("localhost", "127.0.0.1", "::1") or host.endswith(".local"):
            if not config["security"]["allow_localhost"]:
                return "localhost"

        try:
            ip = ipaddress.ip_address(host)
            if _is_blocked_ip(ip) and not config["security"]["allow_private_ips"]:
                return "private_ip"
        except ValueError:
            try:
                resolved = socket.gethostbyname(host)
                ip = ipaddress.ip_address(resolved)
                if _is_blocked_ip(ip) and not config["security"]["allow_private_ips"]:
                    return "private_ip"
            except socket.gaierror:
                return "error"

    except Exception:
        return "error"

    return None

def _url_validator(url: str) -> dict | None:
    if not url:
        return _error_response(None, "missing_url", "URL não informada")

    if len(url) > 2048:
        return _error_response(url, "url_too_long", "URL muito longa")

    if not url.lower().startswith(("http://", "https://")):
        return _error_response(url, "missing_protocol", "URL inválida")

    block = _is_private_or_local(url)

    if block == "localhost":
        return _error_response(url, "localhost_blocked", "Acesso a localhost não permitido")

    if block == "private_ip":
        return _error_response(url, "private_ip_blocked", "Acesso a IPs privados não permitido")

    if block == "error":
        return _error_response(url, "dns_resolution_error", "Não foi possível resolver o host")

    return None

def validate_target(ctx: ScanContext) -> dict | None:
    """
    Valida a URL de entrada. Retorna um dicionário de erro se a URL for inválida ou None se for válida.
        - Se a URL estiver vazia, retorna um erro do tipo "missing_url".
        - Se a URL não começar com "http://" ou "https://", retorna um erro do tipo "missing_protocol".
        - Se a URL for muito longa, retorna um erro do tipo "url_too_long".
        - Se o host resolver para IP privado ou local, retorna erro de bloqueio.
        - Se o DNS falhar ou ocorrer erro inesperado, retorna erro de resolução.
    """
    return _url_validator(ctx.target.url)
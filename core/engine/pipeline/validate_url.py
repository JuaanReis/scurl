from core.models.scan_context import ScanContext
import ipaddress
import socket
from urllib.parse import urlparse
from scurl import config
from importlib.metadata import version
__version__ = version("scurl")

def _is_private_or_local(url: str) -> str | None:
    try:
        host = urlparse(url).hostname
        if not host:
            return None

        if host in ("localhost", "127.0.0.1", "::1") or host.endswith(".local"):
            if not config["security"]["allow_localhost"]:
                return "localhost"

        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private and not config["security"]["allow_private_ips"]:
                return "private_ip"
        except ValueError:
            try:
                resolved = socket.gethostbyname(host)
                ip = ipaddress.ip_address(resolved)
                if ip.is_private and not config["security"]["allow_private_ips"]:
                    return "private_ip"
            except socket.gaierror:
                pass

    except Exception:
        pass

    return None

def _url_validator(url: str) -> dict | None:
    if not url:
        return {
            "status": "error",
            "meta": {
                "url": None,
                "scan_time_s": 0,
                "version": __version__
            },
            "error": {
                "type": "missing_url",
                "message": "URL não informada"
            }
        }

    elif not url.lower().startswith(("http://", "https://")):
        return {
            "status": "error",
            "meta": {
                "url": url,
                "scan_time_s": 0,
                "version": __version__
            },
            "error": {
                "type": "missing_protocol",
                "message": "URL inválida"
            }
        }

    block = _is_private_or_local(url)
    if block == "localhost":
        return {
            "status": "error",
            "meta": {"url": url, "scan_time_s": 0, "version": __version__},
            "error": {"type": "localhost_blocked", "message": "Acesso a localhost não permitido"}
        }
    
    elif block == "private_ip":
        return {
            "status": "error",
            "meta": {"url": url, "scan_time_s": 0, "version": __version__},
            "error": {"type": "private_ip_blocked", "message": "Acesso a IPs privados não permitido"}
        }
    
    elif len(url) > 2048:
        return {
            "status": "error",
            "meta": {
                "url": url,
                "scan_time_s": 0,
                "version": __version__
            },
            "error": {
                "type": "url_too_long",
                "message": "URL muito longa"
            }
        }
    
    else:
        return None

def validate_target(ctx: ScanContext) -> dict | None:
    """
    Valida a URL de entrada. Retorna um dicionário de erro se a URL for inválida ou None se for válida.
        - Se a URL estiver vazia, retorna um erro do tipo "missing_url".
        - Se a URL não começar com "http://" ou "https://", retorna um erro do tipo "missing_protocol".
        - Se a URL for muito longa, retorna um erro do tipo "url_too_long".
    """
    return _url_validator(ctx.target.url)
from core.models.scan_context import ScanContext
from importlib.metadata import version
__version__ = version("scurl")

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
from __init__ import __version__

def url_validator(url: str) -> dict | None:
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
    
    else:
        return None
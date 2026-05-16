from scurl import config
from providers.database.repository import find_by_hash, save_scan

def get_ttl(score: float | None = None) -> int:
    base_ttl = config["cache"]["ttl"]  # 3600

    if score is None:
        return base_ttl
    if score >= 70:
        return 0        
    if score >= 40:
        return 900      
    return base_ttl     

def load_cache(url_hash: str) -> tuple[dict, dict] | None:
    ttl = config["cache"]["ttl"]
    return find_by_hash(url_hash, ttl_seconds=ttl)

def persist_scan(scan_result: dict, target_data: dict) -> None:
    score = scan_result.get("result", {}).get("score")
    if get_ttl(score) == 0:
        return 
    save_scan(scan_result, target_data)
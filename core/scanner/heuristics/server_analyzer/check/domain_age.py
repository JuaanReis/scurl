from datetime import datetime, timezone
from core.models.result_base import ResultBase
from core.math.exponential_decay import domain_age_score

def domain_age(structure: dict) -> ResultBase:
    data = structure.get("rdap")

    if not data:
        return ResultBase(
            value=None,
            normalized=None,
            weight=1.0,
            details={"error": "RDAP data unavailable"}
        )

    creation = _extract_creation_date(data)

    if creation is None:
        return ResultBase(
            value=None,
            normalized=None,
            weight=0.0,
            details={"error": "Creation date not available"}
        )

    now = datetime.now(timezone.utc)
    age = now - creation
    score = domain_age_score(age.days)

    return ResultBase(
        value=age.days,
        normalized=score if score > 0.1 else 0.0,
        weight=4.5,
        details={
            "creation_date": creation.isoformat(),
            "age_days": age.days
        }
    )

def _extract_creation_date(data: dict) -> datetime | None:
    for event in data.get("events", []):
        if event.get("eventAction") == "registration":
            raw = event.get("eventDate")
            if raw:
                return _parse_rdap_date(raw)
    return None

def _parse_rdap_date(raw: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None
from core.models.result_base import ResultBase

def rdap_metadata_incompleteness(structure: dict) -> ResultBase:
    data = structure.get("rdap")

    if not data:
        return ResultBase(
            value=None,
            normalized=None,
            weight=0.0,
            details={"error": "RDAP data unavailable"}
        )

    fields = [
        data.get("entities"),
        data.get("nameservers"),
        data.get("events"),
    ]

    missing = sum(1 for f in fields if f is None)
    score = missing / len(fields)

    return ResultBase(
        value=missing,
        normalized=score,
        weight=2.8,
        details={"missing_fields": missing}
    )
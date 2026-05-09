W = 40

def row(label: str, value: str, width: int = W) -> str:
    value = str(value)
    dots  = "." * max(1, width - len(label) - len(value) - 1)
    return f"{label} {dots} {value}"

def section(title: str):
    print(f"\n{title}")
    print("=" * len(title))

def enabled(val) -> str:
    return "ENABLED" if val else "DISABLED"

def yes_no(val) -> str:
    return "YES" if val else "NO"

def present(val) -> str:
    return "PRESENT" if val else "ABSENT"

def likely(val) -> str:
    return "LIKELY" if val else "UNLIKELY"

def risk_label(val: float) -> str:
    if val <= 0.01:
        return "LOW"
    if val <= 0.3:
        return "MODERATE"
    return "HIGH"
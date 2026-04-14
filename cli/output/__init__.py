from datetime import datetime, timezone
from __init__ import __version__

def print_output(url: str, verbose: bool = False):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"Iniciando Scurl {__version__} (https://github.com/JuaanReis/scurl) em {ts}")
    print(f"Relatório de análise para {url if len(url) <= 70 else url[:67] + "..."}")
    from core.engine.main import run_engine

    data = run_engine(url)

    if data["status"] == "error":
        err = data["error"]
        print(f"FALHA {err['type']}: {err['message']}")
        return

    meta = data["meta"]
    result = data["result"]
    stats = data["stats"]
    heuristics = data["heuristics"]

    skipped = stats["rules_total"] - stats["rules_triggered"]
    if skipped > 0:
        print(f"\nOcultas: {skipped} regras ignoradas (contribuição ≈ 0)")

    if heuristics:
        col_mod  = max(len(h["category"]) for h in heuristics)
        col_rule = max(len(h["name"])     for h in heuristics)
        col_val  = max(len(str(h["value"])) for h in heuristics)

        print(f"\n{'MÓDULO'.ljust(col_mod)}  {'REGRA'.ljust(col_rule)} {'VALOR'.rjust(col_val)}   PESO    CONTRIB")

        for h in heuristics:
            print(
                f"{h['category'].ljust(col_mod).upper()}  "
                f"{h['name'].ljust(col_rule)}  "
                f"{str(h['value']).rjust(col_val)}  "
                f"  {h['weight']:.1f}",
                f"     {h['value'] * h['weight']:.3f}"
            )

            if verbose and h.get("reasons"):
                for reason in h["reasons"]:
                    print(f"{''.ljust(col_mod)}    > {reason}")
    
    if data["insight"]:
        print("\nObservações:")
        for msg in data["insight"]:
            print(f"  * {msg}")

    print(f"\nPontuação: {result['score']}  Risco: {result['risk_level'].upper()}  Veredito: {str(result['verdict']).upper()}")
    print(f"\nScurl concluído: {stats['rules_total']} regras testadas, {stats['rules_triggered']} disparadas — finalizado em {meta['scan_time_s']}s")
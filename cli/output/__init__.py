def print_output(data: dict, verbose: bool = False):
    status = data.get("status")
    if status == "error":
        err: dict = data.get("error", {})
        print(f"FALHA {err.get('type')}: {err.get('message')}")
        return

    meta: dict = data.get("meta", {})
    result: dict = data.get("result", {})
    stats: dict = data.get("stats", {})
    heuristics: list = data.get("heuristics", [])

    skipped = max(0, stats.get("rules_total", 0) - stats.get("rules_triggered", 0))

    if skipped > 0:
        print(f"\nOcultas: {skipped} regras ignoradas (contribuição ≈ 0)")

    if heuristics:
        col_mod  = max(len(str(h.get("category",""))) for h in heuristics)
        col_rule = max(len(h.get("name", "")) for h in heuristics)
        col_val = max(len(str(h.get("value", ""))) for h in heuristics)

        print(f"\n{'MÓDULO'.ljust(col_mod)}  {'REGRA'.ljust(col_rule)} {'VALOR'.rjust(col_val)}   PESO  CONTRIB")

        for h in heuristics:
            print(
                f"{h['category'].ljust(col_mod).upper()}  "
                f"{h['name'].ljust(col_rule)}  "
                f"{str(h['value']).rjust(col_val)}  "
                f"  {h['weight']:.1f}     {h['contribution']}"
            )

            if verbose and h.get("reasons"):
                for reason in h.get("reasons", []):
                    print(f"{''.ljust(col_mod)}    * {reason}")
    
    if data.get("insight"):
        print("\nObservações:")
        for msg in data.get("insight", []):
            print(f"  * {msg}")

    print(
        f"\nPontuação: {result.get('score')}  Risco: {str(result.get('risk_level', '')).upper()}  "
        f"Veredito: {str(result.get('verdict', '')).upper()}"
    )
    print(
        f"Scurl concluído: {stats.get('rules_total', 0)} regras testadas, "
        f"{stats.get('rules_triggered', 0)} disparadas — finalizado em {meta.get('scan_time_s', 0):.2f}s"
    )

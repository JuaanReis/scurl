from core.engine.engine import run_engine
from app.cli.output import print_output
from app.cli.output.store_output import save_output
from .args import parse_args
from importlib.metadata import version
from providers.database.connection import init_db
from sys import exit
__version__ = version("scurl")

def shorten(text, n=56) -> str:
    if not text:
        return ""
    return text if len(text) <= n else text[:n-3] + "..."

def main():
    try:
        init_db()
    except Exception:
        pass
    
    try:
        args = parse_args()
        url = args.url

        if args.output == "-":
            scan, target = run_engine(url, args.k, args.timeout, args.threads, args.retries, use_cache=args.cache)
            save_output("-", scan, target)
            return

        print(f"SCURL :: heuristic web analyzer v{__version__}")
        print("─" * 40)
        scan, target = run_engine(url, args.k, args.timeout, args.threads, args.retries, use_cache=args.cache)

        print_output(scan, target, args.verbose)

        if args.output:
            save_output(args.output, scan, target)
            print(f"\nSaída salva em {args.output}")
    except KeyboardInterrupt:
        exit(0)
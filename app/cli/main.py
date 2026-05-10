from core.engine.engine import run_engine
from app.cli.output import print_output
from app.cli.output.store_output import save_output
from .args import parse_args
from __init__ import __version__

def shorten(text, n=56) -> str:
    if not text:
        return ""
    return text if len(text) <= n else text[:n-3] + "..."

def main():
    args = parse_args()
    url = args.url

    if args.output == "-":
        data = run_engine(url, args.k, args.timeout, args.threads, args.retries, use_cache=args.cache)
        save_output("-", data)
        return

    print(f"SCURL :: heuristic web analyzer v{__version__}")
    print("─" * 40)
    data = run_engine(url, args.k, args.timeout, args.threads, args.retries, use_cache=args.cache)

    print_output(data, args.verbose)

    if args.output:
        save_output(args.output, data)
        print(f"\nSaída salva em {args.output}")

if __name__ == "__main__":
    main()
from core.engine.scurl import run_engine
from .output import print_output
from .args import parse_args
from datetime import datetime, timezone
from __init__ import __version__

def shorten(text, n=56):
    return text if len(text) <= n else text[:n-3] + "..."

def main():
    args = parse_args()
    url = args.url
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"Iniciando Scurl {__version__} (https://github.com/JuaanReis/scurl) em {ts}")
    print(f"Relatório de análise para {shorten(url)}")
    data = run_engine(url, args.thread)
    print_output(data, args.verbose)

if __name__ == "__main__":
    main()
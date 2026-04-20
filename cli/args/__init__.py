from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace | None:
    parse = ArgumentParser(description="scurl CLI version")
    parse.add_argument("--url", "-u", type=str, default="")
    parse.add_argument("--verbose", "-v", action="store_true")
    parse.add_argument("--threads", "-t", type=int, default=1)
    parse.add_argument("--output", "-o", type=str, default="")

    args = parse.parse_args()
    return args
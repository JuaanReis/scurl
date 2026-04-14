from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace | None:
    try:
        parse = ArgumentParser(description="scurl CLI version")
        parse.add_argument("--url", "-u", type=str, default="")
        parse.add_argument("--verbose", "-v", action="store_true")

        args = parse.parse_args()
        return args
    except TypeError:
        return None
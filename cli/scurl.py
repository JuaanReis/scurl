from .output import print_output
from .args import parse_args

def main():
    args = parse_args()
    print_output(args.url, args.verbose)

if __name__ == "__main__":
    main()
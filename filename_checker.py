import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="exif-stripper")
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames to process.",
    )
    args = parser.parse_args(argv)
    results = [filename for filename in args.filenames if not f"{filename}".islower()]
    print("Please avoid using uppercase in filenames", results)
    return len(results)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

import argparse
import logging
import logging.config
import pathlib

from . import snip


def main():
    parser = argparse.ArgumentParser(prog="snip")
    sub_parser = parser.add_subparsers(dest="action", required=True)

    put_parser = sub_parser.add_parser("put")
    put_parser.add_argument("filename")

    get_parser = sub_parser.add_parser("get")
    get_parser.add_argument("filename")
    get_parser.add_argument("vars", nargs="*")

    options = parser.parse_args()
    logging.debug("options: %r", options)

    # TODO: Do not hard code, get from config or ask
    root = pathlib.Path("~/Sync/snip").expanduser()
    root.mkdir(exist_ok=True)

    if options.action == "put":
        snip.put(options.filename, root)
    elif options.action == "get":
        # TODO: make filename optional, use fzf to select
        variables = dict(token.split("=") for token in options.vars)
        logging.debug("variables=%r", variables)
        snip.get(options.filename, root, variables)


if __name__ == "__main__":
    main()

import argparse
import logging
import logging.config
import os
import pathlib
import shutil
import subprocess
import tempfile

from . import __version__, config, snip


def select_file(root: pathlib.Path):
    """Select a file from data dir using fzf."""
    # TODO: Handle case where fzf not found better
    if not shutil.which("fzf"):
        return None

    here = os.getcwd()
    os.chdir(root)

    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stdout:
        subprocess.run(
            ["fzf"],
            text=True,
            stdout=stdout,
        )
        stdout.seek(0)
        selected = stdout.read().strip()
        logging.debug("selected=%r", selected)

    os.chdir(here)
    return selected


def parse_command_line():
    parser = argparse.ArgumentParser(prog="snip")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    sub_parser = parser.add_subparsers(dest="action", required=True)

    # Sub-command: get
    get_parser = sub_parser.add_parser("get")
    get_parser.add_argument("file", nargs="?")
    get_parser.add_argument("-d", "--define", nargs="*", action="extend", default=[])

    # Sub-command: ls
    sub_parser.add_parser("ls")

    # Sub-command: put
    put_parser = sub_parser.add_parser("put")
    put_parser.add_argument("filename")

    options = parser.parse_args()
    logging.debug("options: %r", options)
    return options


def main():
    options = parse_command_line()
    root = config.get_data_dir()

    if options.action == "put":
        snip.put(options.filename, root)
    elif options.action == "ls":
        snip.ls(root)
    elif options.action == "get":
        if options.file is None:
            options.file = select_file(root)
        if options.file is None:
            raise SystemExit("Please specify a file name via -f, or install fzf")
        variables = dict(token.split("=") for token in options.define)
        logging.debug("variables=%r", variables)
        snip.get(options.file, root, variables)


if __name__ == "__main__":
    main()

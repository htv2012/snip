import argparse
import importlib.metadata
import logging
import logging.config
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from . import config, snip
from .pathtools import is_empty_dir

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
LOGGER = logging.getLogger("root.cli")


def select_file(root: pathlib.Path):
    """Select a file from data dir using fzf."""
    if is_empty_dir(root):
        raise ValueError(f"Data directory {root} is empty")

    # TODO: Handle case where fzf not found better
    if not shutil.which("fzf"):
        raise ValueError("fzf is not found, please install")

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
        LOGGER.debug("selected=%r", selected)

    os.chdir(here)
    return selected


def parse_command_line():
    parser = argparse.ArgumentParser(prog="snip")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + importlib.metadata.version("snip"),
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
    LOGGER.debug("options: %r", options)
    return options


def main():
    options = parse_command_line()
    root = config.get_or_create_data_dir()

    if options.action == "put":
        snip.put(options.filename, root)
    elif options.action == "ls":
        snip.ls(root)
    elif options.action == "get":
        try:
            snippet_file = options.file or select_file(root)
        except ValueError as error:
            print(f"{error}", file=sys.stderr)
            return 1
        variables = dict(token.split("=") for token in options.define)
        LOGGER.debug("variables=%r", variables)
        try:
            snip.get(snippet_file, root, variables)
        except FileNotFoundError:
            print(f"Snippet file not found: {snippet_file}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

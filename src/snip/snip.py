#!/usr/bin/env python3
import logging
import logging.config
import pathlib

from . import desktop, editor, minja

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
LOGGER = logging.getLogger("root.snip")


def put(name: str, root: pathlib.Path):
    """Invoke editor to allow the user to create/edit a file."""
    dest = root / name
    editor.edit_file(dest)


def get(name: str, root: pathlib.Path, variables: dict):
    """Get the content of a file, with variables interpolation."""
    dest = root / name
    template = minja.Template(dest.read_text())

    for name in template.names:
        if name not in variables:
            variables[name] = input(f"{name}: ")

    text = template.render(**variables)
    print(text)
    desktop.copy_to_clipboard(text)
    return text


def ls(root: pathlib.Path):
    """List files in root."""
    print(f"Data path: {root}\n")

    paths = sorted(
        path.relative_to(root) for path in root.rglob("*") if not path.is_dir()
    )

    for path in paths:
        print(path)

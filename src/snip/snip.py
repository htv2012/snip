#!/usr/bin/env python3
import logging
import logging.config
import pathlib
import platform
import shutil
import subprocess

from . import editor, minja

__all__ = ["get", "put", "ls"]

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
LOGGER = logging.getLogger("root.snip")


def copy_to_clipboard(text: str):
    """Copy text to the system's clipboard."""
    system = platform.system()
    command = []
    if system == "Darwin":
        command = ["pbcopy"]
    elif system == "Linux":
        if not shutil.which("xsel"):
            LOGGER.warning("xsel not found, cannot copy")
            return
        command = ["xsel", "-b"]
    else:
        LOGGER.warning("System not supported: %s. cannot copy", system)
        return

    subprocess.run(command, text=True, input=text)


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
    copy_to_clipboard(text)
    return text


def ls(root: pathlib.Path):
    """List files in root."""
    print(f"Data path: {root}\n")

    paths = sorted(
        path.relative_to(root) for path in root.rglob("*") if not path.is_dir()
    )

    for path in paths:
        print(path)

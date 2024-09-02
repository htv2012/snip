#!/usr/bin/env python3
import logging
import logging.config
import os
import pathlib
import platform
import shlex
import string
import subprocess
import tempfile
import shutil

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
__all__ = ["get", "put"]


def copy_to_clipboard(text: str):
    system = platform.system()
    command = []
    if system == "Darwin":
        command = ["pbcopy"]
    elif system == "Linux":
        if not shutil.which("xsel"):
            logging.warning("xsel not found, cannot copy")
            return
        command = ["xsel", "-b"]
    else:
        logging.warning("System not supported: %s. Will not copy", system)
        return

    subprocess.run(command, text=True, input=text)


def edit_file(filename, editor=None):
    """
    Invokes an editor to edit a file. If an editor is not specified,
    look up the environment variables EDITOR and then VISUAL. If
    none found, fall back to "nano".

    :param filename: The name of the file
    :param editor: The text editor such as "vim" or "nano"
    """
    editor = editor or os.getenv("EDITOR") or os.getenv("VISUAL") or "nano"
    editor = shlex.split(editor, posix=True)
    subprocess.check_call(editor + [filename])


def edit(text: str, editor: str = None, file_extension: str = None):
    """
    Invokes an editor (see edit_file) to edit some text

    :param text: The block of text to edit
    :param editor: The text editor such as "vim" or "nano"
    :param file_extension: The file extension such as ".txt"
    :return: The edited text
    """
    tmp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=file_extension, delete=False)

    with tmp:
        tmp.write(text)

    try:
        edit_file(tmp.name, editor=editor)
        with open(tmp.name, encoding="utf-8") as stream:
            content = stream.read()
        return content
    finally:
        os.unlink(tmp.name)


def put(name: str, root: pathlib.Path):
    dest = root / name
    edit_file(dest)


def get(name: str, root: pathlib.Path, variables: dict):
    dest = root / name
    template = string.Template(dest.read_text())

    for name in template.get_identifiers():
        if name not in variables:
            variables[name] = input(f"{name}: ")

    text = template.safe_substitute(variables)
    print(text)
    copy_to_clipboard(text)
    return text

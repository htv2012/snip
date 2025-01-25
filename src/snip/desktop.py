#!/usr/bin/env python3
import logging
import logging.config
import pathlib
import platform
import shutil
import subprocess

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
LOGGER = logging.getLogger("root.desktop")


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

import os
import pathlib
import subprocess
import tempfile

from snip.config import load

config = load()

root = pathlib.Path(config["data-dir"])
os.chdir(root)

with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stdout:
    subprocess.run(
        ["fzf"],
        text=True,
        stdout=stdout,
    )
    stdout.seek(0)
    selected = stdout.read().strip()

print(f"{selected=}")

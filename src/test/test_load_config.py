import json
import pathlib

from snip.config import load

CONFIG_PATH = pathlib.Path("~/.config/snip.json").expanduser()
CONFIG_FOUND = CONFIG_PATH.exists()
BAK = CONFIG_PATH.with_suffix(".bak")


def setup_module():
    if CONFIG_FOUND:
        BAK.write_text(CONFIG_PATH.read_text())


def teardown_module():
    if CONFIG_FOUND:
        CONFIG_PATH.write_text(BAK.read_text())


def test_not_exist():
    CONFIG_PATH.unlink(missing_ok=True)
    assert load() == {"data-dir": str(pathlib.Path("~/.local/share/snip").expanduser())}


def test_exist():
    config = {"data-dir": "/tmp"}
    with open(CONFIG_PATH, "w") as stream:
        json.dump(config, stream)

    assert load() == config

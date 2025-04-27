import json
import pathlib

import pytest

from snip.config import get_or_create_data_dir, load

CONFIG_PATH = pathlib.Path("~/.config/snip.json").expanduser()
CONFIG_FOUND = CONFIG_PATH.exists()
BAK = CONFIG_PATH.with_suffix(".bak")


def setup_module():
    if CONFIG_FOUND:
        BAK.write_text(CONFIG_PATH.read_text())


def teardown_module():
    if CONFIG_FOUND:
        CONFIG_PATH.write_text(BAK.read_text())


def test_load_not_exist():
    CONFIG_PATH.unlink(missing_ok=True)
    assert load() == {"data-dir": str(pathlib.Path("~/.local/share/snip").expanduser())}


def test_load_exist():
    config = {"data-dir": "/tmp"}
    with open(CONFIG_PATH, "w") as stream:
        json.dump(config, stream)

    assert load() == config


@pytest.mark.parametrize("exists", [False, True])
def test_get(tmp_path, exists: bool):
    CONFIG_PATH.unlink(missing_ok=True)
    data_dir = tmp_path / "data"
    assert not data_dir.exists()
    assert not data_dir.is_dir()

    if exists:
        data_dir.mkdir()

    config = {"data-dir": str(data_dir)}
    with open(CONFIG_PATH, "w") as stream:
        json.dump(config, stream)

    actual = get_or_create_data_dir()
    assert actual == data_dir
    assert actual.exists()
    assert actual.is_dir()

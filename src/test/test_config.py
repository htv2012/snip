import json
import pathlib

import pytest

import snip.config

HOME_DIR_STR = str(pathlib.Path.home())


def test_config_exists(tmp_path, config_path):
    """Load config when config file exists."""

    # Pre: Ensure a custom config exist
    data_dir = str(tmp_path / "snip-data")
    with open(config_path, "w", encoding="utf-8") as stream:
        json.dump(
            {
                "data-dir": data_dir,
            },
            stream,
        )

    # Act
    config = snip.config.load()

    # Verify
    assert config_path.exists()
    assert pathlib.Path(config["data-dir"]).exists()
    assert config["data-dir"] == str(data_dir)


def test_config_not_exist(config_path):
    """Load config when config file does not exist"""

    # Pre: Ensure config file does not exist
    config_path.unlink(missing_ok=True)

    # Act
    config = snip.config.load()

    # Verify
    assert config_path.exists()
    assert isinstance(config, dict)
    assert "data-dir" in config
    assert pathlib.Path(config["data-dir"]).exists()


@pytest.mark.parametrize(
    "in_path,expected",
    [
        pytest.param("$HOME", HOME_DIR_STR, id="home"),
        pytest.param("${HOME}", HOME_DIR_STR, id="home_in_braces"),
        pytest.param("~", HOME_DIR_STR, id="tilde"),
    ],
)
def test_normalize_path(in_path, expected):
    assert snip.config.normalize_path(in_path) == expected

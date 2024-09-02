import json
import pathlib

from snip.config import load

CONFIG_PATH = pathlib.Path("~/.config/snip.json").expanduser()


def config_prep(tmp_path):
    config_path = pathlib.Path("~/.config/snip.json").expanduser()
    data_dir = tmp_path / "data_dir"

    config = {
        "data-dir": str(data_dir),
        "extra": True,
    }
    with open(config_path, "w", encoding="utf-8") as stream:
        json.dump(config, stream)

    return config_path


def test_config_not_exist():
    """Test load behavior when config file does not exist"""

    # Pre: Ensure config file does not exist
    CONFIG_PATH.unlink(missing_ok=True)

    # Act
    config = load()

    # Verify
    assert CONFIG_PATH.exists()
    assert isinstance(config, dict)
    assert "data-dir" in config
    assert pathlib.Path(config["data-dir"]).exists()


def test_config_exists(tmp_path):
    """Load config when config file exists."""
    # Pre: Ensure a custom config exist
    config_prep(tmp_path)

    config = load()

    # Verify
    assert CONFIG_PATH.exists()
    assert pathlib.Path(config["data-dir"]).exists()
    assert config["extra"] is True

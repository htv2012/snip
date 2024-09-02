import json
import pathlib

from snip.config import load


def test_config_exists(tmp_path, config_path):
    """Load config when config file exists."""

    # Pre: Ensure a custom config exist
    data_dir = str(tmp_path / "snip-data")
    with open(config_path, "w", encoding="utf-8") as stream:
        json.dump(
            {
                "data-dir": data_dir,
                "extra": True,
            },
            stream,
        )

    # Act
    config = load()

    # Verify
    assert config_path.exists()
    assert pathlib.Path(config["data-dir"]).exists()
    assert config["data-dir"] == str(data_dir)
    assert config["extra"] is True


def test_config_not_exist(config_path):
    """Load config when config file does not exist"""

    # Pre: Ensure config file does not exist
    config_path.unlink(missing_ok=True)

    # Act
    config = load()

    # Verify
    assert config_path.exists()
    assert isinstance(config, dict)
    assert "data-dir" in config
    assert pathlib.Path(config["data-dir"]).exists()

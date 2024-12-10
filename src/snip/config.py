import json
import pathlib

DATA_DIR = "data-dir"
DEFAULT_DATA_DIR = pathlib.Path("~/.local/share/snip").expanduser()
DEFAULT_CONFIG = {DATA_DIR: str(DEFAULT_DATA_DIR)}


def load() -> dict:
    """
    Load the configuration file.

    :return: The configuration
    """
    config_path = pathlib.Path("~/.config/snip.json").expanduser()

    if not config_path.exists():
        with open(config_path, "w", encoding="utf-8") as stream:
            json.dump(DEFAULT_CONFIG, stream, indent=4)

    with open(config_path, "r", encoding="utf-8") as stream:
        config = json.load(stream)

    # Ensure this key exists
    config.setdefault(DATA_DIR, str(DEFAULT_DATA_DIR))

    # Ensure the data dir exists
    pathlib.Path(config[DATA_DIR]).mkdir(exist_ok=True)

    return config

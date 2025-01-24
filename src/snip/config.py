import json
import logging
import os
import pathlib
import string

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
LOGGER = logging.getLogger("root.config")

DATA_DIR = "data-dir"
DEFAULT_DATA_DIR = pathlib.Path("~/.local/share/snip").expanduser()
DEFAULT_CONFIG = {DATA_DIR: str(DEFAULT_DATA_DIR)}


def normalize_path(path: str):
    """Normalize the path.

    Convert ~, $HOME, ${HOME} to the home dir
    Expand other environment variables.
    """
    new_path = string.Template(path).substitute(**os.environ)
    new_path = pathlib.Path(new_path).expanduser()
    return str(new_path)


def load() -> dict:
    """
    Load the configuration file.

    :return: The configuration
    """
    config_path = pathlib.Path("~/.config/snip.json").expanduser()
    LOGGER.debug("config_path=%s", config_path)

    if not config_path.exists():
        with open(config_path, "w", encoding="utf-8") as stream:
            json.dump(DEFAULT_CONFIG, stream, indent=4)

    with open(config_path, "r", encoding="utf-8") as stream:
        config = json.load(stream)

    # Ensure this key exists
    # config.setdefault(DATA_DIR, str(DEFAULT_DATA_DIR))
    data_dir = config.get(DATA_DIR, DEFAULT_DATA_DIR)
    # data_dir = string.Template(data_dir).substitute(**os.environ)
    # data_dir = str(pathlib.Path(data_dir).expanduser())
    data_dir = normalize_path(data_dir)
    config[DATA_DIR] = data_dir
    LOGGER.debug("data-dir=%s", config[DATA_DIR])

    # Ensure the data dir exists. Create parent directories if needed
    pathlib.Path(config[DATA_DIR]).mkdir(parents=True, exist_ok=True)

    return config


def get_data_dir() -> pathlib.Path:
    """Load the configuration file and return the data directory."""
    global DATA_DIR
    data = load()
    return pathlib.Path(data[DATA_DIR])

import logging
import logging.config
import pathlib
from typing import Union

logging.config.fileConfig(pathlib.Path(__file__).with_name("logging.ini"))
LOGGER = logging.getLogger("root.cli")


def is_empty_dir(path: Union[str, pathlib.Path]) -> bool:
    """Return True if the directory is empty, False otherwise."""
    path = pathlib.Path(path)
    if not path.is_dir():
        raise ValueError(f"Not a directory: {path}")
    for _ in path.glob("*"):
        return False
    return True

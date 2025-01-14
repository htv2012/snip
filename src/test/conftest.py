import pathlib

import pytest

from snip.minja import Template


@pytest.fixture
def root(tmp_path: pathlib.Path) -> pathlib.Path:
    """Where we can place temp files in tmppath: pathlibfor testing."""
    return tmp_path


@pytest.fixture
def plain_text():
    return "hello world"


@pytest.fixture
def text_file_name(root: pathlib.Path, plain_text):
    """Path to a text file without template.

    This file is pre-populated with some text.
    """
    path = root / "plain.txt"
    path.write_text(plain_text)
    yield path.name
    path.unlink()


@pytest.fixture
def template_text():
    return "{{flowers}} are {{color}}"


@pytest.fixture
def template_text_file(root: pathlib.Path, template_text: str):
    path = root / "template.txt"
    path.write_text(template_text)
    yield path.name
    path.unlink()


@pytest.fixture
def flowers_template(template_text):
    return Template(template_text)


@pytest.fixture(scope="session", autouse=True)
def preserve_config(config_path: pathlib.Path):
    """Preserve the real config file."""
    config_found = config_path.exists()

    # Save state: We rename the config file, so if it was a
    # symbolic link, it got restored as such. Saving by just
    # saving the content does not preserve the link.
    if config_found:
        saved_path = config_path.with_stem("snip-saved")
        saved_path.unlink(missing_ok=True)
        config_path.rename(saved_path)
        config_path.write_bytes(saved_path.read_bytes())

    yield

    # Restore
    if config_found:
        config_path.unlink(missing_ok=True)
        saved_path.rename(config_path)
    else:
        config_path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def config_path() -> pathlib.Path:
    """The path to the config file."""
    path = pathlib.Path("~/.config/snip.json").expanduser()
    return path

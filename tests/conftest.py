import pathlib

import pytest


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
    return "{{flower}} are {{color}}"


@pytest.fixture
def template_text_file(root: pathlib.Path, template_text: str):
    path = root / "template.txt"
    path.write_text(template_text)
    yield path.name
    path.unlink()

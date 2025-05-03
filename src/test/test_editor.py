import os
import pathlib

import pytest

from snip.editor import edit, edit_file

CUSTOM_EDITOR = pathlib.Path(__file__).with_name("custom-editor.sh")
assert CUSTOM_EDITOR.exists()
REFERENCE_TEXT = "Hello, world\n"


@pytest.fixture
def preserve_editor():
    not_set = object()
    editor = os.getenv("EDITOR", not_set)

    yield

    if editor != not_set:
        os.environ["EDITOR"] = editor


def test_edit_file(tmp_path):
    dest = tmp_path / "data.txt"
    assert not dest.exists()

    edit_file(dest, str(CUSTOM_EDITOR))
    assert dest.exists()
    assert dest.read_text() == REFERENCE_TEXT


def test_edit_file_with_env_var(preserve_editor, tmp_path):
    dest = tmp_path / "data.txt"
    assert not dest.exists()

    os.environ["EDITOR"] = str(CUSTOM_EDITOR)
    edit_file(dest)
    assert dest.exists()
    assert dest.read_text() == REFERENCE_TEXT


def test_edit(preserve_editor):
    actual = edit("custom text", editor=str(CUSTOM_EDITOR))
    assert actual == REFERENCE_TEXT


def test_edit_with_env_var(preserve_editor):
    os.environ["EDITOR"] = str(CUSTOM_EDITOR)
    actual = edit("custom text")
    assert actual == REFERENCE_TEXT

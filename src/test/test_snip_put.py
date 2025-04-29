import os
import pathlib

from snip.snip import put

REFERENCE_TEXT = "Hello, world\n"


def setup_module():
    custom_editor = pathlib.Path(__file__).with_name("custom-editor.sh")
    assert custom_editor.exists()

    os.environ["EDITOR"] = str(custom_editor)


def test_put(tmp_path):
    dest = tmp_path / "data.txt"
    assert not dest.exists()

    put(dest.name, root=tmp_path)
    assert dest.exists()
    assert dest.read_text() == REFERENCE_TEXT

import pathlib

import pytest

from snip.pathtools import is_empty_dir

here = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    ["path"],
    [
        pytest.param(here, id="current_path"),
        pytest.param(str(here), id="current_str"),
    ],
)
def test_non_empty(path):
    assert not is_empty_dir(path)


def test_empty(tmp_path):
    dest = tmp_path / "empty"
    dest.mkdir()
    assert is_empty_dir(dest)


def test_file(tmp_path):
    dest = tmp_path / "data.txt"
    dest.write_text("Hello")
    with pytest.raises(ValueError):
        is_empty_dir(dest)

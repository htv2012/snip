import getpass
import os
import pathlib

import pytest

from snip.config import normalize_path

USER = getpass.getuser()


@pytest.mark.parametrize("input_text", ["~", "$HOME", "${HOME}", f"~{USER}"])
def test_home(input_text):
    home = str(pathlib.Path.home())
    assert normalize_path(input_text) == home


@pytest.fixture(params=["$XYZ", "${XYZ}"])
def input_path(request):
    os.environ["XYZ"] = "/bin"
    return request.param


def test_env(input_path):
    assert normalize_path(input_path) == "/bin"

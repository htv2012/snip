"""
Test copy_to_clipboard() function
"""
import shutil
import pathlib

import pytest

from snip.desktop import copy_to_clipboard

SAMPLE_TEXT = "This is a test"


@pytest.fixture
def xsel_found(monkeypatch, tmp_path):
    cat = shutil.which("cat")
    xsel_path = tmp_path / "xsel"
    xsel_path.write_text(f"#!/bin/sh\n{cat}")
    xsel_path.chmod(0o744)

    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setenv("PATH", str(tmp_path))


@pytest.fixture
def darwin_setup(monkeypatch, tmp_path):
    cat = shutil.which("cat")
    xsel_path = tmp_path / "pbcopy"
    xsel_path.write_text(f"#!/bin/sh\n{cat}")
    xsel_path.chmod(0o744)

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setenv("PATH", str(tmp_path))


def test_copy_on_darwin(capfd, darwin_setup):
    copy_to_clipboard(SAMPLE_TEXT)
    assert capfd.readouterr().out == SAMPLE_TEXT


def test_xsel_found(capfd, xsel_found):
    copy_to_clipboard(SAMPLE_TEXT)
    assert capfd.readouterr().out == SAMPLE_TEXT


@pytest.fixture
def setup_command(request, monkeypatch, tmp_path):
    platform_name, tool_name = request.param[0]

    cat = shutil.which("cat")
    xsel_path = tmp_path / tool_name
    xsel_path.write_text(f"#!/bin/sh\n{cat}")
    xsel_path.chmod(0o744)

    monkeypatch.setattr("platform.system", lambda: platform_name)
    monkeypatch.setenv("PATH", str(tmp_path))

@pytest.mark.parametrize(
    "setup_command",
    [
        pytest.param(("Darwin", "pbcopy"), id="macos"),
        pytest.param(("Linux", "xsel"), id="linux"),
    ]
)
def test_found(capfd, setup_command):
    copy_to_clipboard(SAMPLE_TEXT)
    assert capfd.readouterr().out == SAMPLE_TEXT


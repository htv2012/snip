"""
Test copy_to_clipboard() function
"""

import shutil
from unittest import mock

import pytest

from snip.desktop import copy_to_clipboard

SAMPLE_TEXT = "This is a test"


@mock.patch("platform.system", lambda: "Darwin")
@mock.patch("subprocess.run")
def test_on_darwin(mock_run):
    copy_to_clipboard(SAMPLE_TEXT)
    call_args = mock_run.call_args
    assert call_args.args == (["pbcopy"],)
    assert call_args.kwargs["input"] == SAMPLE_TEXT


@mock.patch("platform.system", lambda: "Linux")
@mock.patch("subprocess.run")
def test_on_linux(mock_run):
    copy_to_clipboard(SAMPLE_TEXT)
    call_args = mock_run.call_args
    assert call_args.args == (["xsel", "-b"],)
    assert call_args.kwargs["input"] == SAMPLE_TEXT


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

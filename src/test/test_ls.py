import pytest

from snip.snip import ls


@pytest.fixture
def non_empty_dir(tmp_path):
    target = tmp_path / "data"
    target.mkdir()

    for i in range(3):
        file = target / f"file{i}.txt"
        file.write_text("Hello")

    return target


def test_ls_empty_dir(tmp_path, capfd):
    target = tmp_path / "data"
    target.mkdir()

    ls(target)

    stdout, stderr = capfd.readouterr()
    assert str(target) in stdout
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_ls_non_empty_dir(non_empty_dir, capfd):
    ls(non_empty_dir)

    stdout, stderr = capfd.readouterr()
    assert str(non_empty_dir) in stdout
    assert "file0.txt" in stdout
    assert "file1.txt" in stdout
    assert "file2.txt" in stdout

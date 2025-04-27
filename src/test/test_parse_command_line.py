import pytest

from snip.cli import parse_command_line


@pytest.mark.parametrize(
    ["args"],
    [
        pytest.param([], id="no_args"),
        pytest.param(["foo"], id="wrong_sub_cmd"),
        pytest.param(["-v"], id="show_version"),
        pytest.param(["--version"], id="show_version2"),
        pytest.param(["put"], id="put_without_args"),
    ],
)
def test_parse_expect_raise(args):
    with pytest.raises(SystemExit):
        assert parse_command_line(args)


@pytest.fixture(scope="class")
def actual(request):
    args = request.param
    return parse_command_line(args)


@pytest.mark.parametrize(
    ["actual", "expected"],
    [
        pytest.param(
            ["get"],
            {"action": "get", "file": None, "define": []},
            id="get_without_args",
        ),
        pytest.param(
            ["get", "myfile.txt"],
            {"action": "get", "file": "myfile.txt", "define": []},
            id="get_with_file",
        ),
        pytest.param(
            ["get", "myfile.txt", "-d", "foo=1", "--define", "bar=2"],
            {"action": "get", "file": "myfile.txt", "define": ["foo=1", "bar=2"]},
            id="get_with_defines",
        ),
    ],
    indirect=["actual"],
)
class TestGet:
    def test_action(self, actual, expected):
        assert actual.action == expected["action"]

    def test_file(self, actual, expected):
        assert actual.file == expected["file"]

    def test_define(self, actual, expected):
        assert actual.define == expected["define"]


def test_ls():
    actual = parse_command_line(["ls"])
    assert actual.action == "ls"


def test_put_without_filename():
    with pytest.raises(SystemExit):
        parse_command_line(["put"])


def test_put_with_filename():
    actual = parse_command_line(["put", "myfile"])
    assert actual.action == "put"
    assert actual.filename == "myfile"

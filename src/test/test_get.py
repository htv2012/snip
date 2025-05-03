import io
import sys
from unittest import mock

import snip


def test_plain_text(root, text_file_name: str, plain_text: str):
    assert snip.get(text_file_name, root, {}) == plain_text


@mock.patch.object(sys, "stdin", io.StringIO("blue\n"))
def test_template_without_vars(root, template_text_file: str, template_text: str):
    actual = snip.get(
        name=template_text_file,
        root=root,
        variables={"flowers": "Violets"},
    )
    assert actual == "Violets are blue"


def test_template_with_vars(root, template_text_file: str, template_text: str):
    actual = snip.get(
        name=template_text_file,
        root=root,
        variables={
            "flowers": "Roses",
            "color": "red",
        },
    )
    assert actual == "Roses are red"

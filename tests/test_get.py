from snip import get


def test_plain_text(root, text_file_name: str, plain_text: str):
    assert get(text_file_name, root, {}) == plain_text


def test_template_text(root, template_text_file: str, template_text: str):
    actual = get(
        name=template_text_file,
        root=root,
        variables={
            "flower": "Roses",
            "color": "red",
        },
    )
    assert actual == "Roses are red"

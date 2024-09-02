"""
Test the Template class.
"""

from snip.minja import Template


def test_simple():
    template = Template("{{ flowers }} are {{ color }}")
    assert template.render(color="red", flowers="Roses") == "Roses are red"


def test_load_text():
    template = Template()
    template.load_text("My alias is {{ alias }}")
    assert template.render(alias="anna") == "My alias is anna"


def test_load_text_should_set_names():
    template = Template()
    template.load_text("{{ flowers }} are {{ color }}")
    assert template.names == {"flowers", "color"}


def test_initializer_should_set_names():
    """The initializer must call load_text."""
    template = Template("{{ flowers }} are {{ color }}")
    assert template.names == {"flowers", "color"}


def test_no_duplicate_names():
    """Names should be a set, hence no duplicates."""
    template = Template("{{ a }}, {{ b }}, {{ a }}")
    assert template.names == {"a", "b"}

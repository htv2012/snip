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

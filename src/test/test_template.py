"""
Test the Template class.
"""

import pytest

from snip.minja import Template


def test_simple(flowers_template):
    assert flowers_template.render(color="red", flowers="Roses") == "Roses are red"


def test_load_text():
    template = Template()
    template.load_text("My alias is {{ alias }}")
    assert template.render(alias="anna") == "My alias is anna"


def test_load_text_should_set_names(flowers_template):
    assert flowers_template.names == {"flowers", "color"}


def test_no_duplicate_names():
    """Names should be a set, hence no duplicates."""
    template = Template("{{ a }}, {{ b }}, {{ a }}")
    assert template.names == {"a", "b"}


def test_ignore_spaces_inside_braces():
    """Ensure {{foo}} and {{ foo }} are the same."""
    template = Template("{{foo}},{{ foo }}")
    assert template.render(foo="bar") == "bar,bar"


def test_single_char():
    """Single-char variable such as {{a}}, {{b}}."""
    template = Template("Hello, {{w}}")
    assert template.render(w="world") == "Hello, world"


def test_render_without_key(flowers_template):
    with pytest.raises(KeyError, match="flowers"):
        flowers_template.render()


def test_template_without_braces():
    """Test a template which has no braces."""
    template = Template("Hello, world")
    assert template.render() == "Hello, world"


def test_render_multiple_times(flowers_template):
    """Ensure that expansion works many time."""
    assert flowers_template.render(flowers="Roses", color="red") == "Roses are red"

    with pytest.raises(KeyError, match="color"):
        flowers_template.render(flowers="Violet")


def test_empty_braces():
    """Test empty braces."""
    template = Template("{{}}")
    assert template.render(foo="bar") == "{{}}"

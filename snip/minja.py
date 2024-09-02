"""
Implement a simple template rendering because the default string.Template
is missing function `get_identifiers()` for versions prior to 3.11. The
name `minja` means to be a mini jinja engine.
"""

import re
from typing import Optional

__all__ = ["Template"]


NAME_PATTERN = re.compile(
    r"""
    {{                 # openning double braces
    \s*                # any number of white spaces
    (                  # begin group
        [a-zA-Z_]      # first char of variable
        [a-zA-Z0-9_]*  # subsequent chars
    )                  # end group
    \s*                # any number of white spaces
    }}                 # closing double braces
    """,
    re.VERBOSE,
)


class Template:
    """A simple Jinja-like template rendering class."""

    def __init__(self, text: Optional[str] = None):
        self.names = set()
        self.table = {}
        self.load_text(text or "")

    def load_text(self, text: str):
        self.text = text
        self.names = set(NAME_PATTERN.findall(text))

    def render(self, **kwargs):
        self.table = kwargs
        out = NAME_PATTERN.sub(self._replace, self.text)
        return out

    def _replace(self, match: re.Match) -> str:
        key = match[1]
        out = str(self.table[key])
        return out

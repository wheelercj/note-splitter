"""For splitting an AST into raw text."""


# internal imports
from parser_ import AST
import settings


class Splitter:
    """Creates a Callable that splits an AST into one or more strings."""

    def __call__(self, ast: AST):
        """"""

"""The class definitions for all the tokens.

See the hierarchy of all the token types here:
https://note-splitter.readthedocs.io/en/latest/token-hierarchy.html

Each token class has a ``content`` property. If the token is not a combination of other
tokens, that ``content`` property is a string of the original content of the raw line of
text. Otherwise, the ``content`` property is the list of subtokens. Each token class
also has a boolean class variable (not an instance variable) named ``HAS_PATTERN``. If
``HAS_PATTERN`` is True, the class has a corresponding regular expression in
patterns.py.
"""
import inspect
from abc import ABC
from abc import abstractmethod
from functools import lru_cache
from types import ModuleType
from typing import Any

from note_splitter import patterns


def _get_indentation_level(line: str) -> int:
    """Counts the spaces at the start of the line.

    If there are tabs instead, each tab is counted as 4 spaces. This function assumes
    tabs and spaces are not mixed.
    """
    level = len(line) - len(line.lstrip(" "))
    if not level:
        tab_count = len(line) - len(line.lstrip("\t"))
        level = tab_count * 4
    return level


class Token(ABC):
    """The abstract base class (ABC) for all tokens."""

    HAS_PATTERN = False

    @abstractmethod
    def __init__(self):
        self._content: Any

    def __str__(self):
        """Returns the original content of the token's raw text."""
        return self._content + "\n"

    @property
    def content(self) -> Any:
        pass

    @content.setter
    def content(self, new_content: Any) -> None:
        pass


class Line(Token):
    """The ABC for tokens that take up one line of a file."""

    @abstractmethod
    def __init__(self, line: str = ""):
        self._content = line

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, line: str) -> None:
        self._content = line


class Block(Token):
    """The ABC for tokens that are each a combination of tokens."""

    @abstractmethod
    def __init__(self):
        pass

    @property
    def content(self) -> list[Any]:
        return self._content

    @content.setter
    def content(self, new_content: list[Any]) -> None:
        self._content = new_content

    def __str__(self):
        """Returns the original content of the token's raw text."""
        return "".join([str(token) for token in self._content])

    def __len__(self):
        """Returns the length of the token's content."""
        return len(self._content)

    def __bool__(self):
        """Returns whether the token's content is empty."""
        return bool(self._content)

    def __getitem__(self, index: int) -> Token:
        """Returns the token at the given index."""
        return self._content[index]

    def __setitem__(self, index: int, token: Token) -> None:
        """Sets the token at the given index to the given token."""
        self._content[index] = token

    def __delitem__(self, index: int) -> None:
        """Deletes the token at the given index."""
        del self._content[index]

    def __iter__(self):
        """Returns an iterator for the token's content."""
        return iter(self._content)

    def __contains__(self, item: Token) -> bool:
        """Returns whether the token's content contains an item."""
        return item in self._content

    def insert(self, index: int, token: Token) -> None:
        """Inserts the given token at the given index."""
        self._content.insert(index, token)

    def append(self, token: Token) -> None:
        """Appends the given token to the section."""
        self._content.append(token)

    def remove(self, token: Token) -> None:
        """Removes the given token from the section."""
        self._content.remove(token)


class CanHaveInlineElements(Line):
    """The ABC for single-line tokens that can have inline elements."""

    @abstractmethod
    def __init__(self, line: str = ""):
        self._content = line


class TextListItem(Line):
    """The ABC for text list item tokens."""

    @abstractmethod
    def __init__(self):
        self.level: int


class TablePart(Line):
    """The ABC for tokens that tables are made out of."""

    @abstractmethod
    def __init__(self):
        pass


class Fence(Line):
    """The ABC for tokens that block fences are made out of."""

    @abstractmethod
    def __init__(self):
        pass


class Fenced(Line):
    """The ABC for tokens that are between Fence tokens."""

    @abstractmethod
    def __init__(self):
        pass


class Text(CanHaveInlineElements):
    """Normal text.

    This class is the catch-all for individual lines of text that don't fall into any
    other category.

    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """

    def __init__(self, line: str = ""):
        self._content: str = line
        self.level: int = _get_indentation_level(line)


class EmptyLine(Line):
    """A line with either whitespace characters or nothing.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line


class Header(CanHaveInlineElements):
    """A header (i.e. a title).

    Attributes
    ----------
    content : str
        The content of the line of text.
    body : str
        The content of the line of text not including the header symbol(s) and their
        following whitespace character(s).
    level : int
        The header level. A header level of 1 is the largest possible header.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        self.body: str = line.lstrip("#")
        self.level: int = len(line) - len(self.body)
        self.body = self.body.lstrip()


class HorizontalRule(Line):
    """A horizontal rule.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line


class Blockquote(CanHaveInlineElements):
    """A single-line quote.

    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        self.level: int = _get_indentation_level(line)


class BlockquoteBlock(Block):
    """Multiple lines of blockquotes.

    Attributes
    ----------
    content : list[Blockquote]
        The consecutive blockquote tokens.
    """

    def __init__(self, tokens_: list[Any] = None):
        self._content: list[Any] = tokens_ or []


class Footnote(CanHaveInlineElements):
    """A footnote (not a footnote reference).

    Attributes
    ----------
    content : str
        The content of the line of text.
    reference : str
        The footnote's reference that may appear in other parts of the document.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        if line:
            self.reference: str = line.split(":")[0]
        else:
            self.reference = ""


class Task(TextListItem, CanHaveInlineElements):
    """A to do list item that is either checked or unchecked.

    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    is_done : bool
        Whether the task is done (whether the box is checked).
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        self.level: int = _get_indentation_level(line)
        self.is_done: bool = patterns.finished_task.match(line) is not None


class UnorderedListItem(TextListItem, CanHaveInlineElements):
    """An item in a bullet point list.

    The list can have bullet points as asterisks, minuses, and/or
    pluses.

    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        self.level: int = _get_indentation_level(line)


class OrderedListItem(TextListItem, CanHaveInlineElements):
    """An item in an ordered list.

    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        self.level: int = _get_indentation_level(line)


class TextList(Block):
    """A list that is numbered, bullet-pointed, and/or checkboxed.

    A single text list may have any combination of ordered list items, unordered list
    items, tasks, and other text lists with more indentation.

    Attributes
    ----------
    content : list[Union[TextListItem, "TextList"]]
        The tokens that make up the list. Lists may have sublists.
    level : int
        The number of spaces of indentation of the first item in the list.
    """

    def __init__(self, tokens_: list[Any] = None):
        self._content: list[Any] = tokens_ or []
        if tokens_:
            self.level: int = tokens_[0].level
        else:
            self.level = 0


class TableRow(TablePart):
    """A row of a table.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line


class TableDivider(TablePart):
    """The part of a table that divides the table's header from its
    body.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line


class Table(Block):
    """A table.

    Attributes
    ----------
    content : list[Union[TableRow, TableDivider]]
        The table's row token(s) and possibly divider token(s).
    """

    def __init__(self, tokens_: list[Any] = None):
        self._content: list[Any] = tokens_ or []


class CodeFence(Fence):
    """The delimiter of a multi-line code block.

    Attributes
    ----------
    content : str
        The content of the line of text.
    language : str
        Any text that follows the triple backticks (or triple tildes). Surrounding
        whitespace characters are removed. This will be an empty string if there are no
        non-whitespace characters after the triple backticks/tildes.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line
        self.language: str = line.lstrip("~").lstrip("`").strip()


class Code(Fenced):
    """A line of code inside a code block.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    def __init__(self, line: str = ""):
        self._content: str = line


class CodeBlock(Block):
    """A multi-line code block.

    Attributes
    ----------
    content : list[Union[CodeFence, Code]]
        The code block's code fence tokens surrounding code token(s).
    language : str
        Any text that follows the triple backticks (or tildes) on the line of the
        opening code fence. Surrounding whitespace characters are removed.
    """

    def __init__(self, tokens_: list[Any] = None):
        self._content: list[Any] = tokens_ or []
        if tokens_:
            self.language: str = tokens_[0].language
        else:
            self.language = ""


class MathFence(Fence):
    """The delimiter of a multi-line mathblock.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    HAS_PATTERN = True

    def __init__(self, line: str = ""):
        self._content: str = line


class Math(Fenced):
    """A line of math inside a math block.

    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    def __init__(self, line: str = ""):
        self._content: str = line


class MathBlock(Block):
    """A multi-line mathblock.

    Inline mathblocks are not supported (the opening and closing math fences must be on
    different lines).

    Attributes
    ----------
    content : list[Math]
        The mathblock's math fence tokens surrounding math token(s).
    """

    def __init__(self, tokens_: list[Any] = None):
        self._content: list[Any] = tokens_ or []


class Section(Block):
    """A file section starting with a token of the chosen split type.

    The Splitter returns a list of Sections. Section tokens never contain section
    tokens, but may contain tokens of any and all other types.

    Attributes
    ----------
    content : list[Token]
        The tokens in this section, starting with a token of the chosen split type.
    """

    def __init__(self, tokens_: list[Any] = None):
        self._content: list[Any] = tokens_ or []


def __is_token_type(obj: Any) -> bool:
    """Returns True if obj is a Token type.

    Parameters
    ----------
    obj : Any
        The object to test.
    """
    return inspect.isclass(obj) and obj.__name__ not in ("ABC", "Any", "module")


@lru_cache(maxsize=1)
def get_all_token_types(tokens_module: ModuleType) -> list[type[Token]]:
    """Gets the list of all token types.

    Call the function like this: ``tokens.get_all_token_types(tokens)``.

    Parameters
    ----------
    tokens_module : ModuleType
        The module containing the token types. There is only one correct argument. The
        only reason why the argument is required is because there doesn't seem to be any
        other way to automatically get the list of token types from within the file they
        are in.
    """
    token_types: list[type] = [
        c[1] for c in inspect.getmembers(tokens_module, __is_token_type)
    ]
    for type_ in token_types:
        assert issubclass(type_, Token), f"{type_} is not a token type"
    return token_types

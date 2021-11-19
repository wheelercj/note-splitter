"""The class definitions for all the tokens.

See the hierarchy of all the token types here:  
https://note-splitter.readthedocs.io/en/latest/token-hierarchy.html
"""


import re
from abc import ABC, abstractmethod
from typing import List, Union, Type, Any
from types import ModuleType
import inspect
from functools import lru_cache
from note_splitter import patterns


def _get_indentation_level(line: str) -> int:
    """Counts the spaces at the start of the line.
    
    If there are tabs instead, each tab is counted as 4 spaces. This
    function assumes tabs and spaces are not mixed.
    """
    level = len(line) - len(line.lstrip(' '))
    if not level:
        tab_count = len(line) - len(line.lstrip('\t'))
        level = tab_count * 4
    return level


class Token(ABC):
    """The abstract base class (ABC) for all tokens.
    
    Each non-abstract child class must have a ``content`` attribute. If 
    the token is not a combination of other tokens, that ``content`` 
    attribute must be a string of the original content of the raw line 
    of text. Otherwise, the ``content`` attribute is the list of 
    subtokens.
    """
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        """Returns the original content of the token's raw text."""
        return self.content + '\n'


class Block(Token):
    """The ABC for tokens that are each a combination of tokens.
    
    Each child class must have a ``content`` attribute that is a list
    of the subtokens.
    """
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        """Returns the original content of the token's raw text."""
        return ''.join([str(token) for token in self.content])


class CanHaveInlineElements(Token):
    """The ABC for tokens that can have inline elements.
    
    Each child class must have a ``content`` attribute that is a string.
    Not all tokens with a ``content`` attribute that is a string can 
    have inline elements.
    """    
    @abstractmethod
    def __init__(self):
        pass


class TextListItem(Token):
    """The abstract base class (ABC) for text list item tokens.
    
    Each child class must have ``content`` and ``level`` attributes.
    """
    @abstractmethod
    def __init__(self):
        pass


class TablePart(Token):
    """The ABC for tokens that tables are made out of.
    
    Each child class must have a ``content`` attribute.
    """
    @abstractmethod
    def __init__(self):
        pass


class Fence(Token):
    """The ABC for tokens that block fences are made out of.
    
    Each child class must have a ``content`` attribute.
    """
    @abstractmethod
    def __init__(self):
        pass


class Fenced(Token):
    """The ABC for tokens that are between Fence tokens.

    Each child class must have a ``content`` attribute.
    """
    @abstractmethod
    def __init__(self):
        pass


class Text(CanHaveInlineElements):
    """Normal text.

    This class is the catch-all for text that doesn't fall into any 
    other category.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """
    def __init__(self, line: str):
        self.content: str = line
        self.level: int = _get_indentation_level(line)


class EmptyLine(Token):
    """A line in a file with either whitespace characters or nothing.

    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    pattern: re.Pattern = patterns.empty_line

    def __init__(self, line: str):
        self.content: str = line


class Header(CanHaveInlineElements):
    """A header (i.e. a title).

    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    body : str
        The content of the line of text not including the header 
        symbol(s) and their following whitespace character(s).
    level : int
        The header level. A header level of 1 is the largest possible 
        header.
    """
    pattern: re.Pattern = patterns.header

    def __init__(self, line: str):
        """Parses a line of text and creates a header token."""
        self.content: str = line
        self.body = line.lstrip('#')
        self.level = len(line) - len(self.body)
        self.body = self.body.lstrip()


class HorizontalRule(Token):
    """A horizontal rule.
    
    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    pattern: re.Pattern = patterns.horizontal_rule

    def __init__(self, line: str):
        self.content: str = line


class Blockquote(CanHaveInlineElements):
    """A quote taking up one entire line of text.

    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """
    pattern: re.Pattern = patterns.blockquote

    def __init__(self, line: str):
        self.content: str = line
        self.level: int = _get_indentation_level(line)


class BlockquoteBlock(Block):
    """Multiple lines of blockquotes.
    
    Attributes
    ----------
    content : List[Blockquote]
        The consecutive blockquote tokens.
    """
    def __init__(self, tokens_: List[Blockquote]):
        self.content: list = tokens_


class Footnote(CanHaveInlineElements):
    """A footnote (not a footnote reference).

    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    reference : str
        The footnote's reference that may appear in other parts of the
        document.
    """
    pattern: re.Pattern = patterns.footnote

    def __init__(self, line: str):
        self.content: str = line
        self.reference: str = line.split(':')[0]


class Task(TextListItem, CanHaveInlineElements):
    """A to do list item that is either checked or unchecked.

    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    is_done : bool
        Whether the to do item is done.
    """
    pattern: re.Pattern = patterns.task

    def __init__(self, line: str):
        self.content: str = line
        self.level: int = _get_indentation_level(line)
        self.is_done = patterns.finished_task.match(line) is not None


class UnorderedListItem(TextListItem, CanHaveInlineElements):
    """An item in a bullet point list.
    
    The list can have bullet points as asterisks, minuses, and/or 
    pluses. The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """
    pattern: re.Pattern = patterns.unordered_list_item

    def __init__(self, line: str):
        self.content: str = line
        self.level: int = _get_indentation_level(line)


class OrderedListItem(TextListItem, CanHaveInlineElements):
    """An item in an ordered list.

    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    level : int
        The number of spaces of indentation.
    """
    pattern: re.Pattern = patterns.ordered_list_item

    def __init__(self, line: str):
        self.content: str = line
        self.level: int = _get_indentation_level(line)


class TextList(Block):
    """A list that is numbered, bullet-pointed, and/or checkboxed.
    
    A single text list may have any combination of ordered list items, 
    unordered list items, to dos, and other text lists with more 
    indentation.

    Attributes
    ----------
    content : List[Union[TextListItem, 'TextList']]
        The tokens that make up the list. Lists may have sublists.
    level : int
        The number of spaces of indentation of the first item in the 
        list.
    """
    def __init__(self, tokens_: List[Union[TextListItem, 'TextList']] = []):
        self.content: list = tokens_
        self.level = tokens_[0].level


class TableRow(TablePart):
    """A row of a table.
    
    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    pattern: re.Pattern = patterns.table_row

    def __init__(self, line: str):
        self.content: str = line


class TableDivider(TablePart):
    """The part of a table that divides the table's header from its 
    body.
    
    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    pattern: re.Pattern = patterns.table_divider

    def __init__(self, line: str):
        self.content: str = line


class Table(Block):
    """A table.
    
    Attributes
    ----------
    content : List[Union[TableRow, TableDivider]]
        The table's row token(s) and possibly divider token(s).
    """
    def __init__(self, tokens_: List[Union[TableRow, TableDivider]]):
        self.content: list = tokens_


class CodeFence(Fence):
    """The delimiter of a multi-line code block.
    
    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    language : str
        Any text that follows the triple backticks (or triple tildes). 
        Surrounding whitespace characters are removed. This will be an 
        empty string if there are no non-whitespace characters after the
        triple backticks/tildes.
    """
    pattern: re.Pattern = patterns.code_fence

    def __init__(self, line: str):
        self.content: str = line
        self.language: str = line.lstrip('~').lstrip('`').strip()


class Code(Fenced):
    """A line of code inside a code block.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    def __init__(self, line: str):
        self.content: str = line


class CodeBlock(Block):
    """A multi-line code block.
    
    Attributes
    ----------
    content : List[Union[CodeFence, Code]]
        The code block's code fence tokens surrounding code token(s).
    language : str
        Any text that follows the triple backticks (or tildes) on the
        line of the opening code fence. Surrounding whitespace 
        characters are removed.
    """
    def __init__(self, tokens_: List[Union[CodeFence, Code]]):
        self.content: list = tokens_
        self.language: str = tokens_[0].language


class MathFence(Fence):
    """The delimiter of a multi-line mathblock.
    
    The ``pattern`` attribute is a class attribute.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    pattern: re.Pattern = patterns.math_fence

    def __init__(self, line: str):
        self.content: str = line


class Math(Fenced):
    """A line of math inside a math block.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """
    def __init__(self, line: str):
        self.content: str = line


class MathBlock(Block):
    """A multi-line mathblock.

    Inline mathblocks are not supported (the opening and closing math 
    fences must be on different lines).
    
    Attributes
    ----------
    content : List[Math]
        The mathblock's math fence tokens surrounding math token(s).
    """
    def __init__(self, tokens_: List[Union[MathFence, Math]]):
        self.content: list = tokens_


class Section(Block):
    """A file section starting with a token of the chosen split type.
    
    The Splitter returns a list of Sections. Section tokens never 
    contain section tokens, but may contain tokens of any and all other 
    types.

    Attributes
    ----------
    content : List[Token]
        The tokens in this section, starting with a token of the chosen 
        split type.
    """
    def __init__(self, tokens_: List[Token]):
        self.content: list = tokens_


def __is_token_type(obj: Any) -> bool:
    """Returns True if obj is a Token type.
    
    Parameters
    ----------
    obj : Any
        The object to test.
    """
    return inspect.isclass(obj) and obj.__name__ not in ('ABC', 'module')


@lru_cache(maxsize=1)
def get_all_token_types(tokens_module: ModuleType) -> List[Type[Token]]:
    """Gets the list of all token types.
    
    Call the function like this: ``tokens.get_all_token_types(tokens)``.

    Parameters
    ----------
    tokens_module : ModuleType
        The module containing the token types. There is only one correct
        argument. The only reason why the argument is required is 
        because there doesn't seem to be any other way to automatically 
        get the list of token types from within the file they are in.
    """
    return [c[1] for c in inspect.getmembers(tokens_module, __is_token_type)]

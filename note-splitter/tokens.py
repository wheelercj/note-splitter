# external imports
from abc import ABC
from typing import List


class Token(ABC):
    """The abstract base class (ABC) for all tokens.
    
    Each child class must have a :code:`content` attribute. If the token
    is not a combination of other tokens, that :code:`content` attribute
    must be a string of the original content of the raw line of text.
    """
    
    pass


class Text(Token):
    """Normal text.
    
    May contain tags.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    def __init__(self, line: str):
        self.content = line


class Header(Token):
    """A header (i.e. a title).
    
    May contain tags.

    Attributes
    ----------
    content : str
        The content of the line of text.
    title : str
        The content of the line of text not including the header 
        symbol(s) and their following whitespace character(s).
    level : int
        The header level. A header level of 1 is the largest possible 
        header.
    """
    
    def __init__(self, line: str):
        """Parses a line of text and creates a header token."""
        self.content = line
        self.title = line.lstrip('#')
        self.level = len(line) - len(self.title)
        self.title = self.title.lstrip()


class HorizontalRule(Token):
    """A horizontal rule.
    
    Attributes
    ----------
    content : str
        The content of the line of text.
    """

    def __init__(self, line: str):
        self.content = line


class CodeFence(Token):
    """The delimiter of a multi-line codeblock.
    
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
    
    def __init__(self, line):
        self.content = line
        self.language = line.lstrip('`').strip()


class Codeblock(Token):
    """A multi-line codeblock.
    
    Attributes
    ----------
    content : List[Text]
        The text tokens within the codeblock (between the code fences).
    language : str
        Any text that follows the triple backticks. Surrounding 
        whitespace characters are removed.
    """
    def __init__(self, language: str, content: List[Text]):
        self.content = content
        self.language = language


class Section(Token):
    """A section of a file, starting with a header token.
    
    Section tokens may also contain section tokens, but only ones with a 
    greater header level (a smaller header).

    Attributes
    ----------
    content : List[Token]
        The tokens in this section. This list may be empty.
    header : Header
        The section's header.
    """

    def __init__(self, header: Header, content: List[Token] = []):
        self.content = content
        self.header = header

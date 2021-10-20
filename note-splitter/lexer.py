"""For splitting raw text into a list of tokens.

The lexer categorizes lines of text without looking at their context. 
For example, a markdown codeblock will become two code fence tokens 
surrounding one or more tokens of any type, possibly "incorrect" types 
such as header. After lexing, the token list must be parsed to ensure 
each token has the correct type and to further organize them.

Here are guides for token lists, ASTs, and lexical analysis:

* https://www.twilio.com/blog/abstract-syntax-trees
* https://en.wikipedia.org/wiki/Lexical_analysis
* https://craftinginterpreters.com/scanning.html
"""


# external imports
import re
from typing import List

# internal imports
import tokens


class Lexer:
    """Creates a Callable that converts raw text to a list of tokens."""

    def __call__(self, text: str) -> List[tokens.Token]:
        """Converts raw text to a list of tokens."""
        self.__tokens: List[tokens.Token] = []
        for line in text.split('\n'):
            self.__append_token(line)
        return self.__tokens


    def __append_token(self, line: str) -> None:
        """Parses the text and appends the next token."""
        # Some of the token types cannot be detected yet.
        possible_types = [
            tokens.Header,
            tokens.HorizontalRule,
            tokens.CodeFence,
            tokens.MathFence,
            tokens.Blockquote,
            tokens.ToDo,
            tokens.Done,
            tokens.Footnote,
            tokens.OrderedListItem,
            tokens.UnorderedListItem,
            tokens.TableDivider,
            tokens.TableRow,
        ]

        for type_ in possible_types:
            if self.__is(line, type_.pattern):
                self.__tokens.append(type_(line))
                return


    def __is(self, line: str, pattern: re.Pattern):
        """Determines if the line matches a pattern."""
        return bool(pattern.match(line))

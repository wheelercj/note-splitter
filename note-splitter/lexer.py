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
import patterns


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
        possible_types = [
            (tokens.Header, patterns.any_header),
            (tokens.HorizontalRule, patterns.horizontal_rule),
            (tokens.CodeFence, patterns.code_fence),
            (tokens.MathFence, patterns.math_fence),
            (tokens.Blockquote, patterns.blockquote),
            (tokens.ToDo, patterns.todo),
            (tokens.Done, patterns.done),
            (tokens.Footnote, patterns.footnote),
            (tokens.OrderedListItem, patterns.ordered_list_item),
            (tokens.UnorderedListItem, patterns.unordered_list_item),
            (tokens.TableDivider, patterns.table_divider),
            (tokens.TableRow, patterns.table_row),
        ]

        for type_, pattern in possible_types:
            if self.__is(line, pattern):
                self.__tokens.append(type_(line))
                return


    def __is(self, line: str, pattern: re.Pattern):
        """Determines if the line matches a pattern."""
        return bool(pattern.match(line))

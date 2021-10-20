"""For splitting raw text into a list of tokens.

The lexer only divides lines of text into general categories without
looking at their context. For example, a markdown codeblock will become 
two code fence tokens surrounding one or more tokens of any type, 
possibly "incorrect" types such as header. After lexing, the token list 
must be parsed to ensure each token has the correct type and to further 
organize them.

Here are guides for token lists, ASTs, and lexical analysis:

* https://www.twilio.com/blog/abstract-syntax-trees
* https://en.wikipedia.org/wiki/Lexical_analysis
* https://craftinginterpreters.com/scanning.html
"""


# external imports
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
        if self.__is_any_header(line):
            self.__tokens.append(tokens.Header(line))
        elif self.__is_horizontal_rule(line):
            self.__tokens.append(tokens.HorizontalRule(line))
        elif self.__is_code_fence(line):
            self.__tokens.append(tokens.CodeFence(line))
        else:
            self.__tokens.append(tokens.Text(line))


    def __is_any_header(self, line: str) -> bool:
        """Determines if the line is a header of any level."""
        return bool(patterns.any_header.match(line))


    def __is_horizontal_rule(self, line: str) -> bool:
        """Determines if the line is a horizontal rule."""
        return bool(patterns.horizontal_rule.match(line))


    def __is_code_fence(self, line: str) -> bool:
        """Determines if the line is the start or end of a codeblock."""
        return bool(patterns.code_fence.match(line))

"""For splitting raw text into a list of tokens.

The lexer categorizes lines of text first without looking at their 
context. For example, a markdown codeblock will become two code fence 
tokens surrounding one or more tokens of any type, possibly "incorrect" 
types such as header. Then the lexer makes a quick pass over the token 
list while looking at each token's context to ensure they have the 
correct type.
"""


import re
from typing import List, Type
from note_splitter import tokens


class Lexer:
    """Creates a Callable that converts raw text to a list of tokens."""

    def __call__(self, text: str) -> List[tokens.Token]:
        """Converts raw text to a list of tokens."""
        self.__tokens: List[tokens.Token] = []
        for line in text.split('\n'):
            self.__append_token(line)
        self.__contextualize_tokens()
        return self.__tokens


    def __append_token(self, line: str) -> None:
        """Parses the text and appends the next token."""
        for type_ in tokens.simple_token_types:
            if self.__matches(line, type_.pattern):
                self.__tokens.append(type_(line))
                return
        self.__tokens.append(tokens.Text(line))


    def __matches(self, line: str, pattern: re.Pattern):
        """Determines if the line matches a pattern."""
        return bool(pattern.match(line))


    def __contextualize_tokens(self) -> None:
        """Changes the type of some tokens based on their context."""
        types = [
            (tokens.Code, tokens.CodeFence),
            (tokens.Math, tokens.MathFence),
        ]
        for to_type, wrapper_type in types:
            self.__change_inner_token_types(to_type, wrapper_type)


    def __change_inner_token_types(
            self,
            to_type: Type[tokens.Token],
            wrapper_type: Type[tokens.Token]) -> None:
        """Changes the types of all tokens between tokens of a chosen type.
        
        Changes are made to this class' token list. This function 
        assumes the tokens to change have a ``content`` attribute 
        that is of type ``str``.

        Parameters
        ----------
        to_type : Type[tokens.Token]
            The type to change the inner tokens to.
        wrapper_type : Type[tokens.Token]
            The type of the first and last token.
        """
        in_wrapper = False
        for i, token_ in enumerate(self.__tokens):
            if isinstance(token_, wrapper_type):
                in_wrapper = not in_wrapper
            elif in_wrapper:
                self.__tokens[i] = to_type(token_.content)

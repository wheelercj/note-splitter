"""For splitting raw text into a list of tokens.

The lexer categorizes lines of text first without looking at their
context. For example, a markdown codeblock will become two code fence
tokens surrounding one or more tokens of any type, possibly "incorrect"
types such as header. Then the lexer makes a quick pass over the token
list while looking at each token's context to ensure they have the
correct type.
"""
from typing import List
from typing import Type

from note_splitter import patterns
from note_splitter import settings
from note_splitter import tokens


class Lexer:
    """Creates a Callable that converts raw text to a list of tokens."""

    def __call__(self, text: str) -> List[tokens.Token]:
        """Converts raw text to a list of tokens.

        Parameters
        ----------
        text : str
            The raw text to convert to a list of tokens.
        """
        self.__tokens: List[tokens.Token] = []
        all_token_types = tokens.get_all_token_types(tokens)
        for line in text.split("\n"):
            self.__tokens.append(self.__create_token(line, all_token_types))
        self.__check_token_types()
        return self.__tokens

    def __create_token(self, line: str, all_token_types: List[Type]) -> tokens.Token:
        """Lexes the text, creates a token, and returns it.

        Parameters
        ----------
        line : str
            The line of text to parse.
        all_token_types : List[Type]
            A list of all token types.
        """
        for type_ in all_token_types:
            if type_.HAS_PATTERN and self.__matches(line, type_):
                return type_(line)
        return tokens.Text(line)

    def __matches(self, line: str, type_: Type[tokens.Token]) -> bool:
        """Determines if the line matches the given type's pattern.

        Parameters
        ----------
        line : str
            The line of text to check.
        type_ : Type[tokens.Token]
            The token type to check the pattern of.
        """
        type_name = settings.get_token_type_name(type_).replace(" ", "_")
        if patterns.__dict__[type_name].match(line):
            return True
        return False

    def __check_token_types(self) -> None:
        """Changes the type of some tokens based on their context.

        Changes are made to this class' token list. This function
        assumes the tokens to change have a ``content`` attribute
        that is of type ``str``.
        """
        type_tuples = [
            (tokens.Code, tokens.CodeFence),
            (tokens.Math, tokens.MathFence),
        ]
        for fenced_type, fence_type in type_tuples:
            between_fences = False
            for i, token_ in enumerate(self.__tokens):
                if isinstance(token_, fence_type):
                    between_fences = not between_fences
                elif between_fences:
                    assert isinstance(token_.content, str)
                    self.__tokens[i] = fenced_type(token_.content)

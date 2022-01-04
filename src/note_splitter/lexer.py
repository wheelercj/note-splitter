"""For splitting raw text into a list of tokens.

The lexer categorizes lines of text first without looking at their 
context. For example, a markdown codeblock will become two code fence 
tokens surrounding one or more tokens of any type, possibly "incorrect" 
types such as header. Then the lexer makes a quick pass over the token 
list while looking at each token's context to ensure they have the 
correct type.
"""


from typing import List, Type
from note_splitter import tokens, patterns, settings


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
        for line in text.split('\n'):
            self.__tokens.append(self.__create_token(line, all_token_types))
        self.__check_token_types()
        return self.__tokens


    def __create_token(self,
                       line: str,
                       all_token_types: List[Type]) -> tokens.Token:
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


    def __matches(self,
                  line: str,
                  type_: Type[tokens.Token]) -> bool:
        """Determines if the line matches the given type's pattern.
        
        Parameters
        ----------
        line : str
            The line of text to check.
        type_ : Type[tokens.Token]
            The token type to check the pattern of.
        """
        type_name = settings.get_token_type_name(type_).replace(' ', '_')
        if patterns.__dict__[type_name].match(line):
            return True
        return False


    def __check_token_types(self) -> None:
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

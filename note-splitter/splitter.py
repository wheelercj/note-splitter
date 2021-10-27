"""For splitting an AST's tokens into Sections tokens."""
# settings the splitter requires
# ------------------------------
# split_type : Type
#     The type of the token to split by.
# split_attrs : dict
#     The attributes of the token to split by. If one of the 
#     attributes is named :code:`level`, lesser levels will take
#     precedence in section creation.


# external imports
from typing import List

# internal imports
import tokens
import settings


class Splitter:
    """Creates a Callable that splits tokens into one or more Sections."""

    def __call__(self, tokens_: List[tokens.Token]) -> List[tokens.Section]:
        """"""
        self.__tokens = tokens_
        return self.__get_sections()


    def __get_sections(self) -> List[tokens.Section]:
        """Groups the tokens into section tokens."""
        # Depth-first search for tokens of the chosen split type.
        # Irrelevant tokens are deleted as the loop iterates.
        sections: List[tokens.Section] = []
        while self.__tokens:
            token = self.__tokens[0]
            if self.__should_split(token, False):
                new_section = self.__get_section()
                sections.append(new_section)
            elif isinstance(token.content, list):
                split = Splitter()
                sections.extend(split(token.content))
                self.__tokens.pop(0)
            else:
                self.__tokens.pop(0)

        return sections


    def __get_section(self) -> tokens.Section:
        """Groups some of the tokens into one new section token.
        
        Assumes the first token in the tokens list is of the type that
        was chosen to split by.
        
        If the token type chosen as the section starter has
        a :code:`level` attribute, it must be an integer and lower 
        levels will take precedence over higher levels. E.g., each 
        header token has a level, and larger headers have smaller 
        levels (the largest header possible has a level of 1). When a 
        file is split by headers of level 2, each section (each new 
        file) will start with a header of level 2 and will not contain 
        any other headers of level 2 or any of level 1, but may contain 
        headers of level 3 or greater.
        """
        section_tokens: List[tokens.Token] = []
        section_tokens.append(self.__tokens.pop(0))

        while self.__tokens:
            token = self.__tokens[0]
            if self.__should_split(token):
                return tokens.Section(section_tokens)
            else:
                section_tokens.append(token)
                self.__tokens.pop(0)

        return tokens.Section(section_tokens)


    def __should_split(
            self,
            token: tokens.Token,
            is_splitting: bool = True) -> bool:
        """Determines if a token has certain attributes and values.

        Assumes the token is of the type that was chosen to split by,
        and that the given split attributes exist.

        Parameters
        ----------
        token : tokens.Token
            A token that may be of the type chosen to split by.
        is_splitting : bool
            A boolean for whether splitting is in progress. Used to 
            determine if the tokens should be split just before a token 
            of a lower level than the chosen split level.
        """
        if not isinstance(token, settings.split_type):
            return False
        for key, value in settings.split_attrs.items():
            if is_splitting and key == 'level':
                if token.level > value:
                    return False
            elif getattr(token, key) != value:
                return False
        return True

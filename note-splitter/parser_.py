"""For converting a list of tokens into an abstract syntax tree (AST)."""


# external imports
import re
from typing import List, Optional, Callable, Type, Any
import yaml

# internal imports
import tokens
import patterns


class AST:
    """An entire file as an abstract syntax tree (AST).

    Parameters
    ----------
    tokens_ : List[tokens.Token]
        A list of tokens created from a Lexer object.

    Attributes
    ----------
    frontmatter : Optional[object]
        The file's optional YAML frontmatter as a Python object.
    global_tags : List[str]
        All of the file's tags above any header of level 2 or greater.
    content : List[tokens.Token]
        All the tokens below any frontmatter. The only non-section 
        tokens here are the tokens above all headers.
    """

    def __init__(self, tokens_: List[tokens.Token]):
        if not tokens_:
            return
        self.__tokens = tokens_

        self.frontmatter: Optional[object] = self.__get_group(
                                                self.__load_frontmatter,
                                                patterns.frontmatter_fence,
                                                tokens.Text)
        self.__contextualize_tokens()
        # TODO: create all block tokens here.
        self.global_tags: List[str] = self.__get_global_tags()

        self.content: List[tokens.Token] = []
        
        split_type = tokens.Header
        split_attrs = {'level': 3}  # TODO: get user input
        self.__get_sections(split_type, split_attrs)


    def raw(self) -> str:
        """Returns the original content of the AST's raw text."""
        raw_content = []
        for token in self.content:
            raw_content.append(token.raw())
        return ''.join(raw_content)


    def __contextualize_tokens(self) -> None:
        """Changes the type of some tokens based on their context."""
        types = [
            (tokens.Text, tokens.CodeFence),
            (tokens.Text, tokens.MathFence),
        ]
        for to_type, wrapper_type in types:
            self.__change_inner_token_types(to_type, wrapper_type)


    def __change_inner_token_types(
            self,
            to_type: Type[tokens.Token],
            wrapper_type: Type[tokens.Token]) -> None:
        """Changes the types of all tokens between tokens of a chosen type.
        
        Changes are made to this class' token list. This function 
        assumes the tokens to change have a :code:`content` attribute 
        that is of type :code:`str`.

        Attributes
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


    def __get_group(
            self,
            group_constructor: Callable,
            delimiter_pattern: re.Pattern,
            inner_token_type: Optional[tokens.Token] = None) -> Optional[Any]:
        """Attempts to get a group of related tokens.

        E.g. frontmatter is a "group" because it is two frontmatter 
        fence tokens surrounding one or more text tokens.
        
        Parameters
        ----------
        group_constructor : Callable
            The callable that will be used on the list of the group's 
            tokens, the return value of which will be returned.
        delimiter_pattern : re.Pattern
            The compiled regex pattern of the group's delimiter.
        inner_token_type : Optional[tokens.Token]
            The token type that each token between the group's 
            delimiters should be converted to.
        """
        group_tokens = []
        in_group = False
        while self.__tokens:
            token = self.__tokens[0]

            if token.content == '':
                pass
            elif self.__is(token, delimiter_pattern):
                if in_group:
                    self.__tokens.pop(0)
                    return group_constructor(group_tokens)
                else:
                    in_group = True
            elif in_group:
                if inner_token_type:
                    group_tokens.append(inner_token_type(token.content))
                else:
                    group_tokens.append(token)
            else:
                return None
            
            self.__tokens.pop(0)


    def __is(self, token: tokens.Token, pattern: re.Pattern) -> bool:
        """Determines if a token matches a given pattern."""
        return bool(pattern.match(token.content))


    def __load_frontmatter(
            self,
            tokens_: List[tokens.Text]) -> Optional[object]:
        """Converts Text tokens into a Python object."""
        text: str = '\n'.join([t.content for t in tokens_])
        return yaml.load(text, Loader=yaml.FullLoader)


    def __get_global_tags(self) -> List[str]:
        """Finds all the global tags within the token list.
        
        Assumes the tokens have been contextualized but not yet split 
        into sections. Global tags are tags that are above all headers 
        of level 2 or greater.
        """
        global_tags: List[str] = []
        for token in self.__tokens:
            if isinstance(token, tokens.Header) and token.level >= 2:
                return global_tags
            elif isinstance(token, (tokens.Text, tokens.Header)):
                global_tags.extend(self.__get_tags(token))
        return global_tags


    def __get_tags(self, token: tokens.Token) -> List[str]:
        """Gets the tags in one token."""
        tags = []
        groups = patterns.tags.findall(token.content)
        for group in groups:
            if group[0] in ('', ' ', '\t'):
                tags.append(group[1])
        return tags


    def __get_sections(self, split_type: Type, split_attrs: dict):
        """Groups the tokens into section tokens.
        
        Attributes
        ----------
        split_type : Type
            The type of the token to split by.
        split_attrs : dict
            The attributes of the token to split by. If one of the 
            attributes is named :code:`level`, lesser levels will take
            precedence in section creation.
        """
        is_splitting = False
        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, split_type) \
                    and self.__should_split(token, split_attrs, is_splitting):
                is_splitting = True
                new_section = self.__get_section(split_type, split_attrs)
                self.content.append(new_section)
            else:
                is_splitting = False
                self.__tokens.pop(0)
                self.content.append(token)


    def __get_section(
            self,
            split_type: Type,
            split_attrs: dict) -> tokens.Section:
        """Groups some of the tokens into one new section token.
        
        Assumes the first token in the tokens list is of the type that
        was chosen to split by. A section may contain other sections in 
        some cases.
        
        If the token type chosen as the section starter has
        a :code:`level` attribute, it must be an integer and lower 
        levels will take precedence over higher levels. E.g., each 
        header token has a level, and larger headers have smaller 
        levels (the largest header possible has a level of 1). When a 
        file is split by headers of level 2, each section (each new 
        file) will start with a header of level 2 and will not contain 
        any other headers of level 2 or any of level 1, but may contain 
        headers of level 3 or greater.

        Attributes
        ----------
        split_type : Type
            The type of the token to split by.
        split_attrs : dict
            The attributes of the token to split by. If one of the 
            attributes is named :code:`level`, lesser levels will take
            precedence in section creation.
        """
        section_content: List[tokens.Token] = []
        section_content.append(self.__tokens.pop(0))

        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, split_type):
                if self.__should_split(token, split_attrs):
                    return tokens.Section(section_content)
                else:
                    new_section = self.__get_section(split_type, split_attrs)
                    section_content.append(new_section)
            else:
                section_content.append(token)
            if self.__tokens:
                self.__tokens.pop(0)

        return tokens.Section(section_content)


    def __should_split(
            self,
            token: tokens.Token,
            split_attrs: dict,
            is_splitting: bool = True) -> bool:
        """Determines if a token has certain attributes and values.

        Assumes the token is of the type that was chosen to split by,
        and that the given split attributes exist.

        Attributes
        ----------
        token : tokens.Token
            A token that may be of the type chosen to split by.
        split_attrs : dict
            The attributes of the token to split by. If one of the 
            attributes is named :code:`level`, lesser levels will take
            precedence in section creation.
        is_splitting : bool
            A boolean for whether splitting has already begun. Used to 
            determine if levels of a lower level than the chosen split 
            level should be split.
        """
        for key, value in split_attrs.items():
            if is_splitting and key == 'level':
                if token.level > value:
                    return False
            elif getattr(token, key) != value:
                return False
        return True

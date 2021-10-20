"""For converting a list of tokens into an abstract syntax tree."""


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
        while self.__tokens:
            if isinstance(self.__tokens[0], tokens.Header):
                self.content.append(self.__get_section())
            else:
                self.content.append(self.__tokens.pop(0))


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


    def __load_frontmatter(self, tokens_: List[tokens.Token]) -> object:
        """Converts frontmatter tokens into a Python object."""
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


    def __get_section(self) -> tokens.Section:
        """Gets a section of the file starting with a header.
        
        Assumes the first token in the tokens list is a header token. 
        Every header is the beginning of a new section. A section may 
        contain other sections with greater header levels (smaller 
        headers). Each section ends either when another header of the 
        same or lesser level is found, or at the end of the file.
        """
        # TODO: headers aren't being saved into the AST. The problem is probably in this function.
        # It needs to be generalized for other section starter types anyways.
        section_header = self.__tokens.pop(0)
        section_content: List[tokens.Token] = []
        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, tokens.Header):
                if token.level <= section_header.level:
                    return tokens.Section(section_header, section_content)
                elif token.level > section_header.level:
                    section_content.append(self.__get_section())
            else:
                section_content.append(token)
            if self.__tokens:
                self.__tokens.pop(0)

        return tokens.Section(section_content)

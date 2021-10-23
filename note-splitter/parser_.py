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
        self.content = tokens_

        self.frontmatter: Optional[object] = self.__get_group(
                                                self.__load_frontmatter,
                                                patterns.frontmatter_fence,
                                                tokens.Text)
        self.__contextualize_tokens()
        # TODO: create all block tokens here.
        self.global_tags: List[str] = self.__get_global_tags()


    def __str__(self) -> str:
        """Returns the original content of the AST's raw text."""
        raw_content = []
        for token in self.content:
            raw_content.append(str(token))
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

        Parameters
        ----------
        to_type : Type[tokens.Token]
            The type to change the inner tokens to.
        wrapper_type : Type[tokens.Token]
            The type of the first and last token.
        """
        in_wrapper = False
        for i, token_ in enumerate(self.content):
            if isinstance(token_, wrapper_type):
                in_wrapper = not in_wrapper
            elif in_wrapper:
                self.content[i] = to_type(token_.content)


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
        while self.content:
            token = self.content[0]

            if token.content == '':
                pass
            elif self.__is(token, delimiter_pattern):
                if in_group:
                    self.content.pop(0)
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
            
            self.content.pop(0)


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
        for token in self.content:
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

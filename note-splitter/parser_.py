"""For converting a list of tokens into an abstract syntax tree (AST)."""


# external imports
import re
from typing import List, Optional, Callable, Type, Union
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation

# internal imports
import tokens
import patterns


class AST:
    """An entire file as an abstract syntax tree (AST).

    Parameters
    ----------
    tokens_ : List[tokens.Token]
        A list of tokens created from a Lexer object.
    create_groups : bool
        If True, some of the tokens will be grouped together into larger
        tokens in the resulting AST. Otherwise, the tokens will be left
        as they are and the AST will have frontmatter and global_tags 
        attributes.

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

    def __init__(
            self,
            tokens_: List[tokens.Token],
            create_groups: bool = True):
        if not tokens_:
            return
        self.__tokens = tokens_

        self.frontmatter: Optional[object] = self.__get_frontmatter()
        self.global_tags: List[str] = self.__get_global_tags()
        self.content: List[tokens.Token] = []
        if create_groups:
            self.__create_groups()
        else:
            self.content = self.__tokens
            del self.__tokens


    def __str__(self) -> str:
        """Returns the original content of the AST's raw text."""
        raw_content = []
        for token in self.content:
            raw_content.append(str(token))
        return ''.join(raw_content)


    def __get_frontmatter(self) -> Optional[object]:
        """Gets frontmatter from the tokens list, if it has frontmatter.
        
        If the tokens list does have frontmatter, those tokens are 
        removed from the list and not replaced. Empty lines at the top 
        of the tokens list are discarded.

        Returns
        -------
        Optional[object]
            YAML frontmatter loaded as a Python object. If there is no 
            frontmatter, None will be returned.
        """
        frontmatter_tokens: List[tokens.Token] = []
        in_frontmatter = False
        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, tokens.EmptyLine):
                self.__tokens.pop(0)
            elif self.__matches(token, patterns.frontmatter_fence):
                self.__tokens.pop(0)
                if in_frontmatter:
                    # Remove empty lines below where the frontmatter was.
                    while isinstance(self.__tokens[0], tokens.EmptyLine):
                        self.__tokens.pop(0)
                    return self.__load_frontmatter(frontmatter_tokens)
                else:
                    in_frontmatter = True
            elif in_frontmatter:
                self.__tokens.pop(0)
                frontmatter_tokens.append(token)
            else:
                return None


    def __create_groups(self) -> None:
        """Groups together all tokens that should be grouped together.
        
        No tokens are changed, some are only put together into new 
        tokens. All the tokens will end up in the AST's content 
        attribute, and the __tokens list will be empty.
        """
        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, tokens.TextListItem):
                self.content.append(self.__get_text_list(token.level))
            elif isinstance(token, tokens.Blockquote):
                self.content.append(self.__get_block_of_unique_tokens(
                                        tokens.BlockquoteBlock,
                                        tokens.Blockquote))
            elif isinstance(token, tokens.TablePart):
                self.content.append(self.__get_block_of_unique_tokens(
                                        tokens.Table,
                                        tokens.TablePart))
            elif isinstance(token, tokens.Fence):
                self.content.append(self.__get_fenced_block())
            else:
                self.content.append(token)
                self.__tokens.pop(0)


    def __get_text_list(self, list_level: int) -> tokens.TextList:
        """Creates a token that is a combination of related tokens.
        
        Parameters
        ----------
        list_level : int
            The indentation level (in spaces) of the first item in the 
            list.
        """
        block_tokens: List[tokens.TextListItem] = []
        block_tokens.append(self.__tokens.pop(0))

        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, tokens.TextListItem):
                if token.level > list_level:
                    new_block = self.__get_text_list(token.level)
                    block_tokens.append(new_block)
                elif token.level < list_level:
                    return tokens.TextList(block_tokens)
                else:
                    block_tokens.append(token)
                    self.__tokens.pop(0)
            else:
                break

        return tokens.TextList(block_tokens)


    def __get_block_of_unique_tokens(
            self,
            block_constructor: Callable,
            sub_token_type: Type[tokens.Token]) -> tokens.Token:
        """Creates a token that is a block of specialized tokens.
        
        This is for tokens that have only one purpose: to be part of a 
        block of related tokens. For example, Table tokens are made of 
        TableRow and TableDivider tokens, and those two will never be 
        used for anything else.

        Parameters
        ----------
        block_constructor : Callable
            The constructor for the block of related tokens.
        sub_token_type : Type[tokens.Token]
            The type of the tokens within the block.
        """
        block_tokens: List[sub_token_type] = []
        block_tokens.append(self.__tokens.pop(0))
        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, sub_token_type):
                block_tokens.append(token)
                self.__tokens.pop(0)
            else:
                break
        return block_constructor(block_tokens)


    def __get_fenced_block(self) -> Union[tokens.CodeBlock, tokens.MathBlock]:
        """Creates a code block token or a math block token."""
        block_tokens: List[Union[tokens.Fence, tokens.Code, tokens.Math]] = []
        block_tokens.append(self.__tokens.pop(0))

        while self.__tokens:
            token = self.__tokens[0]
            if type(token) == type(block_tokens[0]):
                block_tokens.append(token)
                self.__tokens.pop(0)
                break
            elif isinstance(token, (tokens.Code, tokens.Math)):
                block_tokens.append(token)
                self.__tokens.pop(0)
            else:
                print('Error: closing fence not found.')

        if isinstance(block_tokens[0], tokens.CodeFence):
            return tokens.CodeBlock(block_tokens)
        return tokens.MathBlock(block_tokens)


    def __matches(self, token: tokens.Token, pattern: re.Pattern) -> bool:
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
        
        Assumes the tokens have been contextualized but not yet combined
        into blocks. Global tags are tags that are above all headers 
        of level 2 or greater.
        """
        global_tags: List[str] = []
        for token in self.__tokens:
            if isinstance(token, tokens.Header) and token.level >= 2:
                return global_tags
            elif isinstance(token, tokens.tag_containing_types):
                global_tags.extend(self.__get_tags(token))
        return global_tags


    def __get_tags(self, token: tokens.Token) -> List[str]:
        """Gets the tags in one token.
        
        Assumes the token's content attribute is a string.
        """
        tags = []
        groups = patterns.tags.findall(token.content)
        for group in groups:
            if group[0] in ('', ' ', '\t'):
                tags.append(group[1])
        return tags

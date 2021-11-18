"""For converting a list of tokens to an abstract syntax tree (AST)."""


import re
from typing import List, Optional, Callable, Type, Union
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation
from note_splitter import tokens, patterns


class AST:
    """An entire file as an abstract syntax tree (AST).

    Attributes
    ----------
    frontmatter : Optional[object]
        The file's optional YAML frontmatter as a Python object.
    global_tags : List[str]
        All of the file's tags above any header of level 2 or greater.
    content : List[tokens.Token]
        All the tokens below any frontmatter.
    footnotes : List[tokens.Footnote]
        All the footnotes in the file.
    """

    def __init__(
            self,
            tokens_: List[tokens.Token],
            create_blocks: bool = True):
        """Creates an AST from a list of tokens.

        Parameters
        ----------
        tokens_ : List[tokens.Token]
            A list of tokens created from a Lexer object.
        create_blocks : bool
            If True, some of the tokens will be grouped together into 
            larger tokens in the resulting AST. Otherwise, the token
            list will be put into the content attribute unchanged. The 
            AST's other attributes will still be created.
        """
        if not tokens_:
            return
        self.__tokens = tokens_  # This attribute empties into self.content.

        self.frontmatter: Optional[object] = self.__get_frontmatter()
        self.global_tags: List[str] = self.__get_global_tags()
        self.footnotes: List[tokens.Footnote] = self.__get_footnotes()
        self.content: List[tokens.Token] = []
        if create_blocks:
            self.__create_blocks()
        else:
            self.content = self.__tokens
        del self.__tokens  # This should be empty if blocks were created.


    def __str__(self) -> str:
        """Returns the original content of the AST's raw text."""
        raw_content = []
        for token in self.content:
            raw_content.append(str(token))
        return ''.join(raw_content)


    def __repr__(self) -> str:
        """Return a string of the type names of the tokens."""
        return ''.join(repr(token) + '\n' for token in self.content)


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


    def __create_blocks(self) -> None:
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
        block_tokens: List[Union[tokens.Fence, tokens.Fenced]] = []
        block_tokens.append(self.__tokens.pop(0))

        while self.__tokens:
            token = self.__tokens[0]
            if type(token) == type(block_tokens[0]):
                block_tokens.append(token)
                self.__tokens.pop(0)
                break
            elif isinstance(token, tokens.Fenced):
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
        """Converts Text tokens into a Python object.
        
        Parameters
        ----------
        tokens_ : List[tokens.Text]
            The tokens that make up the frontmatter.
        """
        text: str = '\n'.join([t.content for t in tokens_])
        return yaml.load(text, Loader=yaml.FullLoader)


    def __get_global_tags(self) -> List[str]:
        """Finds all the global tags within the token list.
        
        Assumes the token types have been checked but that they have not
        yet combined into blocks. Global tags are tags that are above 
        all headers of level 2 or greater.
        """
        global_tags: List[str] = []
        for token in self.__tokens:
            if isinstance(token, tokens.Header) and token.level >= 2:
                return global_tags
            elif isinstance(token, tokens.CanHaveInlineElements):
                global_tags.extend(self.__get_tags(token))
        global_tags = list(set(global_tags))  # Remove duplicates.
        return global_tags


    def __get_footnotes(self) -> List[tokens.Footnote]:
        """Gets the footnotes in the token list."""
        footnotes: List[tokens.Footnote] = []
        for token in self.__tokens:
            if isinstance(token, tokens.Footnote):
                footnotes.append(token)
        return footnotes


    def __get_tags(self, token: tokens.Token) -> List[str]:
        """Gets the tags in one token.
        
        Assumes the token's content attribute is a string.

        Parameters
        ----------
        token : tokens.Token
            The token to get the tags from.
        """
        return patterns.tag.findall(token.content)

"""For converting a list of tokens to an abstract syntax tree (AST)."""
import re
from typing import Any
from typing import Callable
from typing import Union

import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation
from note_splitter import patterns
from note_splitter import tokens


class AST:
    """An entire file as an abstract syntax tree (AST).

    Attributes
    ----------
    frontmatter : object | None
        The file's optional YAML frontmatter as a Python object.
    content : list[tokens.Token]
        All the tokens below any frontmatter.
    footnotes : list[tokens.Footnote]
        All the footnotes in the file.
    """

    def __init__(self, tokens_: list[tokens.Token], parse_blocks: bool = True):
        """Creates an AST from a list of tokens.

        Parameters
        ----------
        tokens_ : list[tokens.Token]
            A list of tokens created from a Lexer object.
        parse_blocks : bool
            If True, some of the tokens will be grouped together into
            larger tokens in the resulting AST. Otherwise, the token
            list will be put into the content attribute unchanged. The
            AST's other attributes will still be created.
        """
        if not tokens_:
            return
        self.__tokens = tokens_  # This attribute empties into self.content.

        self.frontmatter: object | None = self.__get_frontmatter()
        self.footnotes: list[tokens.Footnote] = self.__get_footnotes()
        self.content: list[tokens.Token] = []
        if parse_blocks:
            self.__parse_blocks()
        else:
            self.content = self.__tokens

    def __str__(self) -> str:
        """Returns the original content of the AST's raw text."""
        raw_content = []
        for token in self.content:
            raw_content.append(str(token))
        return "".join(raw_content)

    def __get_frontmatter(self) -> object | None:
        """Gets frontmatter from the tokens list, if it has frontmatter.

        If the tokens list does have frontmatter, those tokens are
        removed from the list and not replaced. Empty lines at the top
        of the tokens list are discarded.

        Returns
        -------
        object | None
            YAML frontmatter loaded as a Python object. If there is no
            frontmatter, None will be returned.
        """
        frontmatter_tokens: list[tokens.Text] = []
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
                assert isinstance(token, tokens.Text)
                frontmatter_tokens.append(token)
            else:
                return None
        return None

    def __parse_blocks(self) -> None:
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
                self.content.append(
                    self.__get_block_of_unique_tokens(
                        tokens.BlockquoteBlock, tokens.Blockquote
                    )
                )
            elif isinstance(token, tokens.TablePart):
                self.content.append(
                    self.__get_block_of_unique_tokens(tokens.Table, tokens.TablePart)
                )
            elif isinstance(token, tokens.Fence):
                self.content.append(self.__get_fenced_block())
            else:
                self.content.append(token)
                self.__tokens.pop(0)

    def __get_text_list(self, indentation_level: int) -> tokens.TextList:
        """Creates a token that is a combination of related tokens.

        Parameters
        ----------
        indentation_level : int
            The indentation level (in spaces) of the first item in the
            list.
        """
        block_tokens: list[Union[tokens.TextList, tokens.TextListItem]] = []
        first_token = self.__tokens.pop(0)
        assert isinstance(first_token, tokens.TextListItem)
        block_tokens.append(first_token)

        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, tokens.TextListItem):
                if token.level > indentation_level:
                    new_block: tokens.TextList = self.__get_text_list(token.level)
                    block_tokens.append(new_block)
                elif token.level < indentation_level:
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
        sub_token_type: Any,
    ) -> tokens.Token:
        """Creates a token that is a block of specialized tokens.

        This is for tokens that have only one purpose: to be part of a
        block of related tokens. For example, Table tokens are made of
        TablePart tokens which will never be used for anything else.

        Parameters
        ----------
        block_constructor : Callable
            The constructor for the block of related tokens.
        sub_token_type : Union[tokens.Blockquote, tokens.TablePart]
            The type of the tokens within the block.
        """
        block_tokens: list[Any] = []
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
        block_tokens: list[Union[tokens.Fence, tokens.Fenced]] = []
        first_token = self.__tokens.pop(0)
        assert isinstance(first_token, tokens.Fence)
        block_tokens.append(first_token)

        while self.__tokens:
            token = self.__tokens[0]
            if isinstance(token, tokens.Fence):
                block_tokens.append(token)
                self.__tokens.pop(0)
                break
            elif isinstance(token, tokens.Fenced):
                block_tokens.append(token)
                self.__tokens.pop(0)
            else:
                print("Error: closing fence not found.")

        if isinstance(block_tokens[0], tokens.CodeFence):
            return tokens.CodeBlock(block_tokens)
        return tokens.MathBlock(block_tokens)

    def __matches(self, token: tokens.Token, pattern: re.Pattern) -> bool:
        """Determines if a token matches a given pattern."""
        assert isinstance(token.content, str)
        return bool(pattern.match(token.content))

    def __load_frontmatter(self, tokens_: list[tokens.Text]) -> object | None:
        """Converts Text tokens into a Python object.

        Parameters
        ----------
        tokens_ : list[tokens.Text]
            The tokens that make up the frontmatter.
        """
        text: str = "\n".join([t.content for t in tokens_])
        return yaml.load(text, Loader=yaml.FullLoader)

    def __get_footnotes(self) -> list[tokens.Footnote]:
        """Gets the footnotes in the token list."""
        footnotes: list[tokens.Footnote] = []
        for token in self.__tokens:
            if isinstance(token, tokens.Footnote):
                footnotes.append(token)
        return footnotes

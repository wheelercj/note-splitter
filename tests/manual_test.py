"""Run this file to see the main steps this program goes through."""
from textwrap import dedent
from typing import Any
from typing import Callable

from note_splitter import tokens
from note_splitter.formatter_ import Formatter
from note_splitter.lexer import Lexer
from note_splitter.parser_ import AST
from note_splitter.settings import load_settings
from note_splitter.settings import settings
from note_splitter.splitter import Splitter


def __manual_test() -> None:
    """Shows the main steps the program goes through on sample markdown."""
    sample_markdown = dedent(
        """
        ---
        title: this is a file with frontmatter
        description: Frontmatter is used to add structured data to a note.
        ---

        # sample markdown
        #first-tag #second-tag
        * bullet point 1
        * bullet point 2

        here is text
        1. ordered
        2. list

        ## second header
        #third-tag
        ```python
        print('this code is inside a code block')
        while True:
            print(eval(input('>>> ')))
        ```

        ### third header
        - [ ] something we need to do
        - [x] something that's done
        > this is
        > a blockquote
        Here's[^1] a footnote reference.

        # fourth header
        The header above is a level 1 header.
        ```cpp
        cout << "here's another code block";
        ```

        [^1]: this is a footnote
        """
    )

    load_settings()
    tokenize: Callable = Lexer()
    tokens_: list[tokens.Token] = tokenize(sample_markdown)
    __print_lexer_output(tokens_)

    settings["parse_blocks"] = True
    ast = AST(tokens_, settings["parse_blocks"])
    __print_parser_output(ast)

    settings["split_type"] = tokens.Header
    settings["split_attrs"] = dict()
    split: Callable = Splitter()
    sections, global_tags = split(ast.content)
    __print_splitter_output(sections, global_tags)

    format_: Callable = Formatter()
    split_contents: list[str] = format_(
        sections, global_tags, ast.frontmatter, ast.footnotes
    )
    __print_formatter_output(split_contents)


def __print_tokens(tokens_: list[Any]) -> None:
    """Prints tokens' types and contents.

    Parameters
    ----------
    tokens_ : list[tokens.Token]
        The list of tokens to print.
    """
    for token in tokens_:
        if isinstance(token.content, list):
            block = __format_tokens(token.content)
            __print_token(token, block)
        else:
            __print_token(token, str(token))


def __print_token(token: tokens.Token, token_content: str) -> None:
    """Prints a token's types and content.

    Parameters
    ----------
    token : tokens.Token
        The token to print.
    token_content : str
        The content of the token to print.
    """
    print(f"{str(type(token).__name__):>18s} | {token_content}", end="")


def __format_tokens(tokens_: list[tokens.Token]) -> str:
    """Formats tokens' contents for test output.

    Parameters
    ----------
    tokens_ : list[tokens.Token]
        The list of tokens to format for printing.
    """
    block = []
    for token in tokens_:
        if isinstance(token.content, list):
            block.append(__format_tokens(token.content))
        else:
            block.append(str(token))
    return (" " * 18 + " | ").join(block)


def __print_lexer_output(tokens_: list[tokens.Token]) -> None:
    """Displays the lexer's output.

    Parameters
    ----------
    tokens_ : list[tokens.Token]
        The list of tokens to print.
    """
    print("**Lexer output:**\n")
    __print_tokens(tokens_)
    input("**Press enter to continue**")


def __print_parser_output(ast: AST) -> None:
    """Displays the parser's output.

    Parameters
    ----------
    ast : AST
        The AST to print.
    """
    print("\n**Parser output:**\n")
    if ast.frontmatter:
        print(f"frontmatter: {ast.frontmatter}\n")
    if ast.footnotes:
        print("footnotes:")
        for footnote in ast.footnotes:
            print(f"  {footnote}")
        print()
    __print_tokens(ast.content)
    input("**Press enter to continue**")


def __print_splitter_output(
    sections: list[tokens.Section], global_tags: list[str]
) -> None:
    """Displays the splitter's output.

    Parameters
    ----------
    sections : list[tokens.Section]
        The list of sections to print.
    global_tags : list[str]
        The list of global tags to print.
    """
    print("\n**Splitter output:**\n")
    __print_tokens(sections)
    print(f"\nglobal tags: {global_tags}\n")
    input("**Press enter to continue**")


def __print_formatter_output(split_contents: list[str]) -> None:
    """Displays the formatter's output.

    Parameters
    ----------
    split_contents : list[str]
        The list of strings to print. Each string represents one new
        file's content.
    """
    print("\n**Formatter output:**\n")
    for i, text in enumerate(split_contents):
        print(f"**file {i}:**\n{text}")


if __name__ == "__main__":
    __manual_test()

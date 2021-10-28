# external imports
from typing import List, Callable
from textwrap import dedent

# internal imports
import settings
import tokens
from lexer import Lexer
from parser_ import AST
from splitter import Splitter
from formatter_ import Formatter


def test():
    sample_markdown = dedent(
        '''
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
        #third-tag <- not a global tag
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

        # fourth header
        The header above is a level 1 header.
        ```cpp
        cout << "here's another code block";
        ```
        ''')

    tokenize: Callable = Lexer()
    tokens_: List[tokens.Token] = tokenize(sample_markdown)
    print_lexer_output(tokens_)

    settings.create_groups = True
    ast = AST(tokens_, settings.create_groups)
    print_parser_output(ast)

    settings.split_type = tokens.Header
    settings.split_attrs = dict()
    split: Callable = Splitter()
    sections: List[tokens.Section] = split(ast.content,
                                           settings.split_type,
                                           settings.split_attrs)
    print_splitter_output(sections)

    # format: Callable = Formatter()
    # split_contents: List[str] = format(sections,
    #                                    ast.global_tags,
    #                                    ast.frontmatter)
    # print_formatter_output(split_contents)


def print_tokens(tokens_: List[tokens.Token]) -> None:
    """Prints tokens' types and contents."""
    for token in tokens_:
        if isinstance(token.content, list):
            block = format_tokens(token.content)
            print_token(token, block)
        else:
            print_token(token, str(token))


def print_token(token: tokens.Token, token_content: str) -> None:
    """Prints a token's types and content."""
    print(f'{str(type(token)):>34s} | {token_content}', end='')


def format_tokens(tokens_: List[tokens.Token]) -> str:
    """Formats tokens' contents for test output."""
    block = []
    for token in tokens_:
        if isinstance(token.content, list):
            block.append(format_tokens(token.content))
        else:
            block.append(str(token))
    return (' ' * 34 + ' | ').join(block)


def print_lexer_output(tokens_: List[tokens.Token]) -> None:
    """Display's the lexer's output."""
    print('**Lexer output:**\n')
    print_tokens(tokens_)
    input('**Press enter to continue**')


def print_parser_output(ast: AST) -> None:
    """Display's the parser's output."""
    print('\n**Parser output:**\n')
    if ast.frontmatter:
        print(f'frontmatter: {ast.frontmatter}\n')
    if ast.global_tags:
        print(f'global tags: {ast.global_tags}\n')
    print_tokens(ast.content)
    input('**Press enter to continue**')


def print_splitter_output(sections: List[tokens.Section]) -> None:
    """Display's the splitter's output."""
    print('\n**Splitter output:**\n')
    print_tokens(sections)
    input('**Press enter to continue**')


def print_formatter_output(split_contents: List[str]) -> None:
    """Display's the formatter's output."""
    print('\n**Formatter output:**\n')
    for i, text in enumerate(split_contents):
        print(f'**file {i}:\n{text}')

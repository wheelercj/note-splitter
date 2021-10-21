# external imports
from typing import List, Callable
from textwrap import dedent

# internal imports
import tokens
from lexer import Lexer
from parser_ import AST


def test_tokenization():
    # TODO: use a testing framework (pytest?) instead of this.

    sample_markdown = dedent(
        '''
        ---
        title: this is a file with frontmatter
        description: Frontmatter is used to add structured data to a note. More details here https://assemble.io/docs/YAML-front-matter.html
        ---

        # sample markdown
        #first-tag #second-tag

        * bullet point 1
        * bullet point 2

        here is text

        1. ordered
        2. list

        ## second header
        #third-tag <- this tag should not be considered a global tag because it's below a header of a level > 1

        ```python
        print('this code is inside a code block')
        while True:
            print(eval(input('>>> ')))
        ```

        ### third header
        - [ ] to do
        - [x] done

        > this is
        > a blockquote

        #### fourth header
        ```cpp
        cout << "here's another code block";
        ```
        ''')

    tokenize: Callable = Lexer()
    tokens_: List[tokens.Token] = tokenize(sample_markdown)
    ast = AST(tokens_)

    if ast.frontmatter:
        print(f'frontmatter:\n{ast.frontmatter}\n')
    if ast.global_tags:
        print(f'global tags:\n{ast.global_tags}\n')
    
    print_ast(ast)


def print_ast(ast: AST):
    """Print's an ast's tokens' types and contents."""
    tokens_: List[tokens.Token] = ast.content
    for token in tokens_:
        if isinstance(token, tokens.Section):
            print(' ' * 10 + "<class 'tokens.Section'> |" + '-' * 80)
            print_ast(token)
        else:
            print_token(token)


def print_token(token: tokens.Token):
    """Prints a token's type and content."""
    print(f'{str(type(token)):>34s} | {token.raw()}', end='')

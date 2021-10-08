# external imports
from typing import List, Callable
from textwrap import dedent

# internal imports
from tokens import Token, Lexer


def test_tokenization():
    # TODO: use a testing framework (pytest?) instead of this.

    sample_markdown = dedent(
        '''
        ---
        title: this is a file with frontmatter
        description: Frontmatter is used to add structured data to a note. More details here: https://assemble.io/docs/YAML-front-matter.html
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
    tokens: List[Token] = tokenize(sample_markdown)
    for token in tokens:
        print('------------------------------')
        print(f'token.type_ = {token.type_}')
        print(f'token.content = {token.content}')

import datetime
from textwrap import dedent

from note_splitter import parser_
from note_splitter import tokens


################
#  SyntaxTree  #
################


def test_SyntaxTree_with_frontmatter():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.Text("---"),
            tokens.Text("title: Hello, world!"),
            tokens.Text("---"),
            tokens.Header("# Hello, world!"),
            tokens.Text("This is a test."),
        ]
    )
    assert syntax_tree.frontmatter == {"title": "Hello, world!"}
    assert str(syntax_tree) == dedent(
        """\
        # Hello, world!
        This is a test.
        """
    )
    assert isinstance(syntax_tree.content[0], tokens.Header)
    assert isinstance(syntax_tree.content[1], tokens.Text)


def test_SyntaxTree_with_code_block():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.Header("# Hello, world!"),
            tokens.Text("This is a test."),
            tokens.EmptyLine(""),
            tokens.CodeFence("```python"),
            tokens.Code('print("hey")'),
            tokens.CodeFence("```"),
        ]
    )
    assert str(syntax_tree) == dedent(
        """\
        # Hello, world!
        This is a test.

        ```python
        print("hey")
        ```
        """
    )
    assert isinstance(syntax_tree.content[0], tokens.Header)
    assert isinstance(syntax_tree.content[1], tokens.Text)
    assert isinstance(syntax_tree.content[2], tokens.EmptyLine)
    assert isinstance(syntax_tree.content[3], tokens.CodeBlock)


def test_SyntaxTree_with_table():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.TableRow("| a | b | c |"),
            tokens.TableDivider("|---|---|---|"),
            tokens.TableRow("| 1 | 2 | 3 |"),
            tokens.EmptyLine(""),
            tokens.Header("# Hello, world!"),
        ]
    )
    assert str(syntax_tree) == dedent(
        """\
        | a | b | c |
        |---|---|---|
        | 1 | 2 | 3 |

        # Hello, world!
        """
    )
    assert isinstance(syntax_tree.content[0], tokens.Table)
    assert isinstance(syntax_tree.content[1], tokens.EmptyLine)
    assert isinstance(syntax_tree.content[2], tokens.Header)


def test_SyntaxTree_with_text_list():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.UnorderedListItem("* This is an unordered list item."),
            tokens.Task("- [ ] This is a task."),
            tokens.OrderedListItem("1. This is an ordered list item."),
            tokens.Task("- [x] This is another task."),
            tokens.EmptyLine(""),
            tokens.Header("# Hello, world!"),
        ]
    )
    assert str(syntax_tree) == dedent(
        """\
        * This is an unordered list item.
        - [ ] This is a task.
        1. This is an ordered list item.
        - [x] This is another task.

        # Hello, world!
        """
    )
    assert isinstance(syntax_tree.content[0], tokens.TextList)
    assert isinstance(syntax_tree.content[1], tokens.EmptyLine)
    assert isinstance(syntax_tree.content[2], tokens.Header)


#####################
#  __get_text_list  #
#####################


def test___get_text_list():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.UnorderedListItem("* This is an unordered list item."),
            tokens.OrderedListItem("1. This is an ordered list item."),
            tokens.Task("- [ ] This is a task."),
            tokens.Text("This is text."),
        ],
        parse_blocks=False,
    )
    text_list = syntax_tree._SyntaxTree__get_text_list(indentation_level=0)
    assert str(text_list) == dedent(
        """\
        * This is an unordered list item.
        1. This is an ordered list item.
        - [ ] This is a task.
        """
    )


def test___get_text_list_with_varying_indentation():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.OrderedListItem("1. This is an ordered list item."),
            tokens.OrderedListItem("    187. second list item."),
            tokens.OrderedListItem("        1189. third list item."),
            tokens.Text("This is text."),
        ],
        parse_blocks=False,
    )
    text_list = syntax_tree._SyntaxTree__get_text_list(indentation_level=0)
    assert str(text_list) == dedent(
        """\
        1. This is an ordered list item.
            187. second list item.
                1189. third list item.
        """
    )
    assert isinstance(text_list[0], tokens.OrderedListItem)
    assert text_list[0].level == 0
    assert isinstance(text_list[1], tokens.TextList)
    assert text_list[1][0].level == 4
    assert isinstance(text_list[1][1], tokens.TextList)
    assert text_list[1][1][0].level == 8


##################################
#  __get_block_of_unique_tokens  #
##################################


def test___get_block_of_unique_tokens_with_blockquotes():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.Blockquote("> This is a blockquote."),
            tokens.Blockquote("> This is another blockquote."),
            tokens.Header("# Hello, world!"),
            tokens.Text("This is a test."),
        ],
        parse_blocks=False,
    )
    block = syntax_tree._SyntaxTree__get_block_of_unique_tokens(
        tokens.BlockquoteBlock, tokens.Blockquote
    )
    assert str(block) == dedent(
        """\
        > This is a blockquote.
        > This is another blockquote.
        """
    )


def test___get_block_of_unique_tokens_with_table_parts():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.TableRow("| a | b | c |"),
            tokens.TableDivider("|---|---|---|"),
            tokens.TableRow("| 1 | 2 | 3 |"),
            tokens.Header("# Hello, world!"),
            tokens.Text("This is a test."),
        ],
        parse_blocks=False,
    )
    block = syntax_tree._SyntaxTree__get_block_of_unique_tokens(
        tokens.Table, tokens.TablePart
    )
    assert str(block) == dedent(
        """\
        | a | b | c |
        |---|---|---|
        | 1 | 2 | 3 |
        """
    )


########################
#  __get_fenced_block  #
########################


def test___get_fenced_block_with_code_block():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.CodeFence("```python"),
            tokens.Code('print("hey")'),
            tokens.CodeFence("```"),
            tokens.Header("# Hello, world!"),
            tokens.Text("This is a test."),
        ],
        parse_blocks=False,
    )
    block = syntax_tree._SyntaxTree__get_fenced_block()
    assert str(block) == dedent(
        """\
        ```python
        print("hey")
        ```
        """
    )


def test___get_fenced_block_with_math_block():
    syntax_tree = parser_.SyntaxTree(
        [
            tokens.MathFence("$$"),
            tokens.Math("x^2"),
            tokens.MathFence("$$"),
            tokens.Header("# Hello, world!"),
            tokens.Text("This is a test."),
        ],
        parse_blocks=False,
    )
    block = syntax_tree._SyntaxTree__get_fenced_block()
    assert str(block) == dedent(
        """\
        $$
        x^2
        $$
        """
    )


########################
#  __load_frontmatter  #
########################


def test___load_frontmatter():
    text_tokens = [
        tokens.Text("title: Hello, world!"),
        tokens.Text("date: 2020-01-01"),
    ]
    assert parser_.SyntaxTree([])._SyntaxTree__load_frontmatter(text_tokens) == {
        "title": "Hello, world!",
        "date": datetime.date(2020, 1, 1),
    }

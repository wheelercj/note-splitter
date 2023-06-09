import re
from textwrap import dedent

from note_splitter import patterns
from note_splitter import split_tab
from note_splitter import tokens
from note_splitter.formatter_ import Formatter
from note_splitter.lexer import Lexer
from note_splitter.splitter import Splitter


################
#  split_text  #
################


def test_split_text_with_nothing():
    assert [] == split_tab.split_text(
        content="",
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.Header,
        split_attrs={},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=False,
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
    )


def test_split_text_with_headers():
    content = dedent(
        """\
        # first header
        Here is a sentence.
        # second header
        Here is another sentence.
        """
    )
    result: list[str] = split_tab.split_text(
        content=content,
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.Header,
        split_attrs={},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=False,
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
    )
    expected = [
        dedent(
            """\
        # first header
        Here is a sentence.
        """
        ),
        dedent(
            """\
        # second header
        Here is another sentence.

        """
        ),
    ]
    assert result == expected


def test_split_text_with_blocks():
    content = dedent(
        """\
        # first header

        ```python
        print('hello')
        # python comment, not a header
        ```

        # second header

        $$
        5 + 5
        $$
        """
    )
    result: list[str] = split_tab.split_text(
        content=content,
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.Header,
        split_attrs={},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=True,
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
    )
    expected = [
        dedent(
            """\
        # first header

        ```python
        print('hello')
        # python comment, not a header
        ```

        """
        ),
        dedent(
            """\
        # second header

        $$
        5 + 5
        $$

        """
        ),
    ]
    assert result == expected


def test_split_text_with_elements_to_copy():
    content = dedent(
        """\
        ---
        title: note title here
        date: 2020-01-01
        ---

        # first header
        #tag1 #tag2

        ```python
        print('hello')
        # python comment, not a header
        ```

        [^1]: this is a footnote

        ## second header

        $$
        5 + 5
        $$

        Here[^1] is a sentence.
        """
    )
    result: list[str] = split_tab.split_text(
        content=content,
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.Header,
        split_attrs={"level": 2},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=True,
        copy_global_tags=True,
        copy_frontmatter=True,
        move_footnotes=True,
    )
    expected = [
        dedent(
            """\
        ---
        date: 2020-01-01
        title: second header
        ---

        # second header
        #tag1 #tag2

        $$
        5 + 5
        $$

        Here[^1] is a sentence.

        [^1]: this is a footnote
        """
        )
    ]
    assert result == expected


def test_split_text_with_top_ordered_list_items():
    content = dedent(
        """\
        # first header

        1. first item
            1. first subitem
            2. second subitem
        2. second item
        3. third item
            1. first subitem
        """
    )
    result: list[str] = split_tab.split_text(
        content=content,
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.OrderedListItem,
        split_attrs={"level": 0},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=True,
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
    )
    expected = [
        dedent(
            """\
        1. first item
            1. first subitem
            2. second subitem
        """
        ),
        dedent(
            """\
        2. second item
        """
        ),
        dedent(
            """\
        3. third item
            1. first subitem
        """
        ),
    ]
    assert result == expected


def test_split_text_with_all_ordered_list_items():
    content = dedent(
        """\
        # first header

        1. first item
            1. first subitem
            2. second subitem
        2. second item
        3. third item
            1. third subitem
        """
    )
    result: list[str] = split_tab.split_text(
        content=content,
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.OrderedListItem,
        split_attrs={},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=False,
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
    )
    expected = [
        "1. first item\n",
        "    1. first subitem\n",
        "    2. second subitem\n",
        "2. second item\n",
        "3. third item\n",
        "    1. third subitem\n\n",
    ]
    assert result == expected


def test_split_text_with_custom_pattern():
    content = dedent(
        """\
        # first header

        1.first item without leading space
            1.first subitem
            2. second subitem
        2. second item
        3.third item
            1. third subitem
        """
    )
    ordered_list_item_pattern = patterns.ordered_list_item
    patterns.__dict__["ordered_list_item"] = re.compile(r"^\s*\d+[.)]\s*.*$")
    assert patterns.ordered_list_item != ordered_list_item_pattern
    result: list[str] = split_tab.split_text(
        content=content,
        tokenize=Lexer(),
        split=Splitter(),
        format_=Formatter(),
        split_type=tokens.OrderedListItem,
        split_attrs={"level": 0},
        using_split_keyword=False,
        remove_split_keyword=False,
        split_keyword="",
        parse_blocks=False,
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
    )
    patterns.__dict__["ordered_list_item"] = ordered_list_item_pattern
    expected = [
        dedent(
            """\
        1.first item without leading space
            1.first subitem
            2. second subitem
        """
        ),
        dedent(
            """\
        2. second item
        """
        ),
        dedent(
            """\
        3.third item
            1. third subitem

        """
        ),
    ]
    assert result == expected

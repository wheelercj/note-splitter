import pytest
import re
from typing import List, Tuple, Callable
from textwrap import dedent
from note_splitter import main, lexer, splitter, formatter_, tokens, patterns
from note_splitter.settings import settings


@pytest.fixture
def callables() -> Tuple[Callable]:
    tokenize = lexer.Lexer()
    split = splitter.Splitter()
    format_ = formatter_.Formatter()
    settings["using_split_keyword"] = False
    settings["copy_global_tags"] = False
    settings["copy_frontmatter"] = False
    settings["move_footnotes"] = False
    return tokenize, split, format_


################
#  split_text  #
################


def test_split_text_with_nothing(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
    settings["parse_blocks"] = False
    settings["split_type"] = tokens.Header
    settings["split_attrs"] = {}
    result: List[str] = main.split_text("", tokenize, split, format_)
    assert result == []


def test_split_text_with_headers(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
    content = dedent(
        """\
        # first header
        Here is a sentence.
        # second header
        Here is another sentence.
        """
    )
    settings["parse_blocks"] = False
    settings["split_type"] = tokens.Header
    settings["split_attrs"] = {}
    result: List[str] = main.split_text(content, tokenize, split, format_)
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


def test_split_text_with_blocks(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
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
    settings["parse_blocks"] = True
    settings["split_type"] = tokens.Header
    settings["split_attrs"] = {}
    result: List[str] = main.split_text(content, tokenize, split, format_)
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


def test_split_text_with_elements_to_copy(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
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
    settings["parse_blocks"] = True
    settings["split_type"] = tokens.Header
    settings["split_attrs"] = {"level": 2}
    settings["copy_global_tags"] = True
    settings["copy_frontmatter"] = True
    settings["move_footnotes"] = True
    result: List[str] = main.split_text(content, tokenize, split, format_)
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


def test_split_text_with_top_ordered_list_items(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
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
    settings["parse_blocks"] = True
    settings["split_type"] = tokens.OrderedListItem
    settings["split_attrs"] = {"level": 0}
    result: List[str] = main.split_text(content, tokenize, split, format_)
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


def test_split_text_with_all_ordered_list_items(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
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
    settings["parse_blocks"] = False
    settings["split_type"] = tokens.OrderedListItem
    settings["split_attrs"] = {}
    result: List[str] = main.split_text(content, tokenize, split, format_)
    expected = [
        "1. first item\n",
        "    1. first subitem\n",
        "    2. second subitem\n",
        "2. second item\n",
        "3. third item\n",
        "    1. third subitem\n\n",
    ]
    assert result == expected


def test_split_text_with_custom_pattern(callables: Tuple[Callable]):
    tokenize, split, format_ = callables
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
    settings["parse_blocks"] = False
    settings["split_type"] = tokens.OrderedListItem
    settings["split_attrs"] = {"level": 0}
    settings["ordered_list_item_pattern"] = r"^\s*\d+[.)]\s*.*$"
    patterns.__dict__["ordered_list_item"] = re.compile(
        settings["ordered_list_item_pattern"]
    )
    result: List[str] = main.split_text(content, tokenize, split, format_)
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

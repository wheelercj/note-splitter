import re
from textwrap import dedent
from typing import Callable

import pytest
from note_splitter import home_tab
from note_splitter import patterns
from note_splitter.formatter_ import Formatter
from note_splitter.lexer import Lexer
from note_splitter.splitter import Splitter
from PySide6 import QtCore


@pytest.fixture
def callables() -> tuple[Lexer, Splitter, Formatter]:
    tokenize = Lexer()
    split = Splitter()
    format_ = Formatter()
    settings = QtCore.QSettings()
    settings.setValue("using_split_keyword", False)
    settings.setValue("copy_global_tags", False)
    settings.setValue("copy_frontmatter", False)
    settings.setValue("move_footnotes", False)
    return tokenize, split, format_


################
#  split_text  #
################


def test_split_text_with_nothing(callables: tuple[Callable, Callable, Callable]):
    tokenize, split, format_ = callables
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", False)
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {})
    result: list[str] = home_tab.split_text("", tokenize, split, format_)
    assert result == []


def test_split_text_with_headers(callables: tuple[Callable, Callable, Callable]):
    tokenize, split, format_ = callables
    content = dedent(
        """\
        # first header
        Here is a sentence.
        # second header
        Here is another sentence.
        """
    )
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", False)
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {})
    result: list[str] = home_tab.split_text(content, tokenize, split, format_)
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


def test_split_text_with_blocks(callables: tuple[Callable, Callable, Callable]):
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
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", True)
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {})
    result: list[str] = home_tab.split_text(content, tokenize, split, format_)
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


def test_split_text_with_elements_to_copy(
    callables: tuple[Callable, Callable, Callable]
):
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
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", True)
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {"level": 2})
    settings.setValue("copy_global_tags", True)
    settings.setValue("copy_frontmatter", True)
    settings.setValue("move_footnotes", True)
    result: list[str] = home_tab.split_text(content, tokenize, split, format_)
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


def test_split_text_with_top_ordered_list_items(
    callables: tuple[Callable, Callable, Callable]
):
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
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", True)
    settings.setValue("split_type", "ordered list item")
    settings.setValue("split_attrs", {"level": 0})
    result: list[str] = home_tab.split_text(content, tokenize, split, format_)
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


def test_split_text_with_all_ordered_list_items(
    callables: tuple[Callable, Callable, Callable]
):
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
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", False)
    settings.setValue("split_type", "ordered list item")
    settings.setValue("split_attrs", {})
    result: list[str] = home_tab.split_text(content, tokenize, split, format_)
    expected = [
        "1. first item\n",
        "    1. first subitem\n",
        "    2. second subitem\n",
        "2. second item\n",
        "3. third item\n",
        "    1. third subitem\n\n",
    ]
    assert result == expected


def test_split_text_with_custom_pattern(callables: tuple[Callable, Callable, Callable]):
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
    settings = QtCore.QSettings()
    settings.setValue("parse_blocks", False)
    settings.setValue("split_type", "ordered list item")
    settings.setValue("split_attrs", {"level": 0})
    settings.setValue("ordered_list_item_pattern", r"^\s*\d+[.)]\s*.*$")
    patterns.__dict__["ordered_list_item"] = re.compile(
        settings.value("ordered_list_item_pattern")
    )
    result: list[str] = home_tab.split_text(content, tokenize, split, format_)
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

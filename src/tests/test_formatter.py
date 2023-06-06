from textwrap import dedent

import pytest
from note_splitter import formatter_
from note_splitter import tokens


##############
#  __call__  #
##############


def test_format_section_with_empty_section():
    format = formatter_.Formatter()
    section = tokens.Section()
    assert [] == format(
        sections=[section],
        global_tags=[],
        copy_global_tags=False,
        copy_frontmatter=False,
        move_footnotes=False,
        frontmatter=None,
        footnotes=None,
    )


def test_format():
    format = formatter_.Formatter()
    sections = [
        tokens.Section(
            [
                tokens.Header("# This is a title"),
                tokens.Text("This is text."),
                tokens.Header("## This is a sub-title"),
                tokens.Text("This is[^1] text."),
            ]
        ),
        tokens.Section(
            [
                tokens.Header("## second section's title"),
                tokens.Text("abcdefghi."),
                tokens.Header("### jaklfd;sfaldfjlksj"),
                tokens.Text("text."),
            ]
        ),
    ]
    global_tags = ["#tag1", "#tag2"]
    frontmatter = {
        "title": "This is a title",
        "author": "This is the author",
    }
    footnotes = [tokens.Footnote("[^1]: This is a footnote.")]
    result = format(
        sections=sections,
        global_tags=global_tags,
        copy_global_tags=True,
        copy_frontmatter=True,
        move_footnotes=True,
        frontmatter=frontmatter,
        footnotes=footnotes,
    )
    expected = [
        dedent(
            """\
            ---
            author: This is the author
            title: This is a title
            ---

            # This is a title
            #tag1 #tag2
            This is text.
            ## This is a sub-title
            This is[^1] text.
            [^1]: This is a footnote.
        """
        ),
        dedent(
            """\
            ---
            author: This is the author
            title: second section's title
            ---

            # second section's title
            #tag1 #tag2
            abcdefghi.
            ## jaklfd;sfaldfjlksj
            text.
        """
        ),
    ]
    assert result == expected


#######################
#  normalize_headers  #
#######################


def test_normalize_headers():
    section = tokens.Section(
        [
            tokens.Header("## This is a title"),
            tokens.Text("This is some text"),
            tokens.Header("### This is a sub-title"),
            tokens.Header("### This is a sub-sub-title"),
        ]
    )
    formatter_.Formatter().normalize_headers(section)
    assert len(section) == 4
    content = "\n".join(
        [section[0].content, section[1].content, section[2].content, section[3].content]
    )
    assert (
        content == "# This is a title\n"
        "This is some text\n"
        "## This is a sub-title\n"
        "## This is a sub-sub-title"
    )


def test_normalize_headers_with_empty_section():
    section = tokens.Section()
    with pytest.raises(IndexError):
        formatter_.Formatter().normalize_headers(section)


def test_normalize_headers_with_normal_headers():
    section = tokens.Section(
        [
            tokens.Header("# This is a title"),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
            tokens.Header("## This is another title"),
        ]
    )
    formatter_.Formatter().normalize_headers(section)
    assert len(section) == 4
    content = "\n".join(
        [section[0].content, section[1].content, section[2].content, section[3].content]
    )
    assert (
        content == "# This is a title\n"
        "Here[^1] is a footnote reference.\n"
        "This is text in a section.\n"
        "## This is another title"
    )


########################
#  insert_global_tags  #
########################


def test_insert_global_tags_into_empty_section():
    section = tokens.Section()
    formatter_.Formatter().insert_global_tags(["#tag1", "#tag2"], section)
    assert len(section) == 1
    assert isinstance(section[0], tokens.Text)
    assert section[0].content == "#tag1 #tag2"


def test_insert_global_tags_after_header():
    section = tokens.Section(
        [
            tokens.Header("# title"),
        ]
    )
    formatter_.Formatter().insert_global_tags(["#tag1", "#tag2"], section)
    assert len(section) == 2
    assert isinstance(section[0], tokens.Header)
    assert section[0].content == "# title"
    assert isinstance(section[1], tokens.Text)
    assert section[1].content == "#tag1 #tag2"


def test_insert_global_tags_with_no_header():
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    formatter_.Formatter().insert_global_tags(["#tag1", "#tag2"], section)
    assert len(section) == 4
    content = "\n".join(
        [section[0].content, section[1].content, section[2].content, section[3].content]
    )
    assert (
        content == "#tag1 #tag2\nThis is text in a section.\n"
        "Here[^1] is a footnote reference.\n"
        "This is text in a section."
    )


#######################
#  get_section_title  #
#######################


def test_get_section_title_without_header():
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    assert "This is text in a section." == formatter_.Formatter().get_section_title(
        section
    )


def test_get_section_title_with_empty_line():
    section = tokens.Section(
        [
            tokens.EmptyLine(""),
            tokens.Text("This is text in a section."),
        ]
    )
    assert "This is text in a section." == formatter_.Formatter().get_section_title(
        section
    )


def test_get_section_title_with_header():
    section = tokens.Section(
        [
            tokens.Header("# This is a title"),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    assert "This is a title" == formatter_.Formatter().get_section_title(section)


def test_get_section_title_with_header_after_text():
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Header("# This is a title"),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    assert "This is a title" == formatter_.Formatter().get_section_title(section)


def test_get_section_title_with_empty_section():
    section = tokens.Section()
    title = formatter_.Formatter().get_section_title(section)
    # title should be a UUID4 hash
    assert len(title) == 36


#########################
#  prepend_frontmatter  #
#########################


def test_prepend_frontmatter():
    frontmatter = {
        "title": "original title.",
        "author": "Bob",
    }
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    formatter_.Formatter().prepend_frontmatter(frontmatter, "new title", section)
    assert len(section) == 4
    assert section[0].content == "---\nauthor: Bob\ntitle: new title\n---\n"
    assert section[1].content == "This is text in a section."
    assert section[2].content == "Here[^1] is a footnote reference."
    assert section[3].content == "This is text in a section."


def test_prepend_frontmatter_without_frontmatter():
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    formatter_.Formatter().prepend_frontmatter(None, "new title", section)
    assert len(section) == 3
    assert section[0].content == "This is text in a section."
    assert section[1].content == "Here[^1] is a footnote reference."
    assert section[2].content == "This is text in a section."


####################
#  move_footnotes  #
####################


def test_move_footnotes_with_missing_footnote():
    footnote = tokens.Footnote("[^1]: This is a footnote.")
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    formatter_.Formatter().move_footnotes([footnote], section)
    assert footnote in section


def test_move_footnotes_with_extra_footnote():
    footnote = tokens.Footnote("[^1]: This is a footnote.")
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("This is text in a section."),
            footnote,
        ]
    )
    formatter_.Formatter().move_footnotes([footnote], section)
    for token in section:
        assert not isinstance(token, tokens.Footnote)
    assert len(section) == 2


def test_move_footnotes_with_no_change_required():
    footnote = tokens.Footnote("[^1]: This is a footnote.")
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
            footnote,
        ]
    )
    formatter_.Formatter().move_footnotes([footnote], section)
    assert footnote in section
    assert len(section) == 4


####################################
#  footnote_referenced_in_section  #
####################################


def test_footnote_referenced_in_section():
    footnote = tokens.Footnote("[^1]: This is a footnote.")
    section = tokens.Section(
        [
            tokens.Text("This is text in a section."),
            tokens.Text("Here[^1] is a footnote reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    assert formatter_.footnote_referenced_in_section(footnote, section)


def test_footnote_referenced_in_section_with_long_footnote_name():
    footnote = tokens.Footnote("[^long name & spaces]: This is a footnote.")
    section = tokens.Section(
        [
            tokens.Blockquote("> This is a quote in a section."),
            tokens.Task("- [ ] Here[^long name & spaces] is a reference."),
            tokens.Text("This is text in a section."),
        ]
    )
    assert formatter_.footnote_referenced_in_section(footnote, section)

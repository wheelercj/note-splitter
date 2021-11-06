import pytest
from note_splitter import patterns


@pytest.mark.parametrize('test_input', [
    (''),
    ('      '),
    ('\t'),
    ('   \t  '),
])
def test_empty_lines(test_input):
    assert patterns.empty_line.match(test_input)


@pytest.mark.parametrize('test_input', [
    ('non-empty line'),
    ('      .     '),
])
def test_non_empty_lines(test_input):
    assert not patterns.empty_line.match(test_input)


@pytest.mark.parametrize('test_input', [
    ('# first level header'),
    ('## second level header'),
    ('### third level header'),
    ('#### fourth level header'),
    ('##### fifth level header'),
    ('###### sixth level header'),
    ('####### seventh level header'),
    ('#      header with extra spaces   '),
])
def test_headers(test_input):
    assert patterns.any_header.match(test_input)


@pytest.mark.parametrize('test_input', [
    ('#tag'),
    ('##double-tag'),
    ('> ##### quoted title'),
    (' # spaced title'),
    ('    # indented title'),
    ('a# letter in front of title'),
    ('normal text'),
])
def test_non_headers(test_input):
    assert not patterns.any_header.match(test_input)


@pytest.mark.parametrize('test_input', [
    ('#tag'),
    (' #spaced '),
    ('\t#tabbed\t'),
    ('##double-tag'),
    ('#with_underscore'),
    ('#with-ending-hash#'),
    ('#ümläuts'),
    ('##中国人'),
])
def test_tags(test_input):
    assert patterns.tag.findall(test_input)


@pytest.mark.parametrize('test_input', [
    ('# header'),
    ('\\#escaped-tag'),
    ('example.com/test#anchor-name'),
    ('someword#withahashinside'),
    ('!#negatedtag'),
    ('#tag@hey'),
])
def test_non_tags(test_input):
    assert not patterns.tag.findall(test_input)

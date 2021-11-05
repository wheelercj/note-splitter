import pytest
from note_splitter import patterns


@pytest.mark.parametrize('pattern, test_input', [
    (patterns.empty_line, ''),
    (patterns.empty_line, ' '),
    (patterns.empty_line, '\t'),

    (patterns.any_header, '# first level header'),
    (patterns.any_header, '## second level header'),
    (patterns.any_header, '### third level header'),
    (patterns.any_header, '#### fourth level header'),
    (patterns.any_header, '##### fifth level header'),
    (patterns.any_header, '###### sixth level header'),
    (patterns.any_header, '####### seventh level header'),

    (patterns.any_header, '#      header with extra spaces in front'),
    (patterns.any_header, '## header with spaces after     '),
])
def test_all_patterns_match(pattern, test_input):
    assert pattern.match(test_input) is not None


@pytest.mark.parametrize('pattern, test_input', [
    (patterns.empty_line, 'non-empty line'),

    (patterns.any_header, ' # fake header with a space at the start of the line'),
])
def test_all_patterns_do_not_match(pattern, test_input):
    assert pattern.match(test_input) is None

from note_splitter import lexer
from note_splitter import tokens


def test_tokenize():
    line = "# This is a header"
    tokenize = lexer.Lexer()
    token = tokenize(line)[0]
    assert isinstance(token, tokens.Header)


def test_tokenize_with_text():
    line = "This is text"
    tokenize = lexer.Lexer()
    token = tokenize(line)[0]
    assert isinstance(token, tokens.Text)


def test_tokenize_with_text_and_header():
    line = "# This is a header\nThis is text"
    tokenize = lexer.Lexer()
    tokens_ = tokenize(line)
    assert len(tokens_) == 2
    assert isinstance(tokens_[0], tokens.Header)
    assert isinstance(tokens_[1], tokens.Text)


def test_tokenize_with_tag_in_footnote():
    line = "[^1]: This is a footnote with a #tag"
    tokenize = lexer.Lexer()
    tokens_ = tokenize(line)
    assert isinstance(tokens_[0], tokens.Footnote)


def test_tokenize_with_code_block():
    content = "```\nThis is a code block\n```"
    tokenize = lexer.Lexer()
    tokens_ = tokenize(content)
    assert len(tokens_) == 3
    assert isinstance(tokens_[0], tokens.CodeFence)
    assert isinstance(tokens_[1], tokens.Code)
    assert isinstance(tokens_[2], tokens.CodeFence)

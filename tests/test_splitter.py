from note_splitter import tokens
from note_splitter.splitter import Splitter


##################
# __should_split #
##################


def test___should_split_wrong_type():
    s = Splitter()
    assert not s._Splitter__should_split(tokens.Text(), tokens.Header, {})


def test___should_split_right_type():
    s = Splitter()
    assert s._Splitter__should_split(tokens.CodeFence(), tokens.CodeFence, {})


def test___should_split_greater_level():
    s = Splitter()
    assert not s._Splitter__should_split(tokens.Header('## header'),
                                         tokens.Header,
                                         {'level': 1})


def test___should_split_lesser_level():
    s = Splitter()
    assert s._Splitter__should_split(tokens.Header('## header'),
                                     tokens.Header,
                                     {'level': 3})


def test___should_split_equal_level():
    s = Splitter()
    assert s._Splitter__should_split(tokens.Header('## header'),
                                     tokens.Header,
                                     {'level': 2})


def test___should_split_wrong_value():
    s = Splitter()
    assert not s._Splitter__should_split(tokens.Text('hi'),
                                         tokens.Text,
                                         {'content': 'bye'})


def test___should_split_right_value():
    s = Splitter()
    assert s._Splitter__should_split(tokens.Text('hi'),
                                     tokens.Text,
                                     {'content': 'hi'})

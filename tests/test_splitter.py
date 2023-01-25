from note_splitter import tokens
from note_splitter.splitter import Splitter
from PySide6 import QtCore


##################
# __should_split #
##################


def test___should_split_wrong_type():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {})
    s = Splitter()
    assert not s._Splitter__should_split(tokens.Text())


def test___should_split_right_type():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "code fence")
    settings.setValue("split_attrs", {})
    s = Splitter()
    assert s._Splitter__should_split(tokens.CodeFence())


def test___should_split_greater_level():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {"level": 1})
    s = Splitter()
    assert not s._Splitter__should_split(tokens.Header("## header"))


def test___should_split_lesser_level():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {"level": 3})
    s = Splitter()
    assert s._Splitter__should_split(tokens.Header("## header"))


def test___should_split_equal_level():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "header")
    settings.setValue("split_attrs", {"level": 2})
    s = Splitter()
    assert s._Splitter__should_split(tokens.Header("## header"))


def test___should_split_with_unindented_ordered_list_item():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "ordered list item")
    settings.setValue("split_attrs", {"level": 0})
    s = Splitter()
    assert s._Splitter__should_split(tokens.OrderedListItem("1. first item"))


def test___should_split_with_indented_ordered_list_item():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "ordered list item")
    settings.setValue("split_attrs", {"level": 0})
    s = Splitter()
    assert not s._Splitter__should_split(tokens.OrderedListItem("    2. second item"))


def test___should_split_wrong_value():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "text")
    settings.setValue("split_attrs", {"content": "bye"})
    s = Splitter()
    assert not s._Splitter__should_split(tokens.Text("hi"))


def test___should_split_right_value():
    settings = QtCore.QSettings()
    settings.setValue("split_type", "text")
    settings.setValue("split_attrs", {"content": "hi"})
    s = Splitter()
    assert s._Splitter__should_split(tokens.Text("hi"))

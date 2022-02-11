from abc import ABC
from note_splitter import tokens


############################
#  _get_indentation_level  #
############################


def test__get_indentation_level():
    assert 4 == tokens._get_indentation_level("    ")
    assert 8 == tokens._get_indentation_level("        ")
    assert 12 == tokens._get_indentation_level("            ")
    assert 16 == tokens._get_indentation_level("                ")


#####################
#  __is_token_type  #
#####################


def test___is_token_type():
    assert tokens.__is_token_type(tokens.Blockquote)


def test___is_token_type_with_string():
    assert not tokens.__is_token_type("this isn't even a type")


def test___is_token_type_with_type_that_is_not_a_token_type():
    assert not tokens.__is_token_type(ABC)


#########################
#  get_all_token_types  #
#########################


def test_get_all_token_types():
    all_token_types = tokens.get_all_token_types(tokens)
    assert len(all_token_types) >= 28
    assert tokens.Blockquote in all_token_types

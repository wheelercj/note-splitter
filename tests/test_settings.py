import pytest
from note_splitter import settings, tokens


##########################
#  get_token_type_names  #
##########################


def test_get_token_type_names():
    all_token_type_names = settings.get_token_type_names()
    assert 28 <= len(all_token_type_names)
    assert "token" in all_token_type_names


def test_get_token_type_names_with_invalid_token_type_name():
    with pytest.raises(TypeError):
        settings.get_token_type_name("This function doesn't take strings.")


def test_get_token_type_with_blockquote():
    predicate = lambda token_type: not issubclass(token_type, tokens.Blockquote)
    assert tokens.Blockquote not in settings.get_token_type_names(predicate)


#########################
#  get_token_type_name  #
#########################


def test_get_token_type_name_with_code_fence():
    assert "code fence" == settings.get_token_type_name(tokens.CodeFence)


def test_get_token_type_name_with_blockquote():
    assert "blockquote" == settings.get_token_type_name(tokens.Blockquote)


####################
#  get_token_type  #
####################


def test_get_token_type():
    assert tokens.CodeFence == settings.get_token_type("code fence")


def test_get_token_type_with_invalid_token_type():
    with pytest.raises(ValueError):
        settings.get_token_type("invalid")

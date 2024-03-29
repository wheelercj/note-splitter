import os
from datetime import datetime

from note_splitter import note


####################
#  create_file_id  #
####################


def test_create_14_digit_id():
    file_id = note.create_file_id(r"%Y%M%D%h%m%s", "", datetime.now())
    assert len(file_id) == 14
    for char in file_id:
        assert char.isdigit()


def test_create_12_digit_id():
    file_id = note.create_file_id(r"%Y%M%D%h%m", "# sample title", datetime.now())
    assert len(file_id) == 12
    for char in file_id:
        assert char.isdigit()


def test_create_uuid():
    file_id = note.create_file_id(r"%uuid4", "## hey", datetime.now())
    assert len(file_id) == 36
    for char in file_id:
        assert char.isalnum() or char == "-"


def test_create_id_from_header():
    file_id = note.create_file_id(r"%title", "# this is a title", datetime.now())
    assert file_id == "this is a title"


def test_create_id_from_header_2():
    file_id = note.create_file_id(r"%title", "##   a title  ", datetime.now())
    assert file_id == "a title"


def test_create_id_from_lower_header():
    file_id = note.create_file_id(
        r"%title", "here is a line of text\n### title on second line", datetime.now()
    )
    assert file_id == "title on second line"


def test_create_id_from_line():
    file_id = note.create_file_id(
        r"%title", "line of text\nanother line", datetime.now()
    )
    assert file_id == "line of text"


def test_create_id_from_custom_format():
    file_id = note.create_file_id(r"%Y-%M-%D_%h:%m:%s", "", datetime.now())
    assert len(file_id) == 19
    for char in file_id:
        assert char.isdigit() or char in ("-", "_", ":")


def test_create_id_from_duplicate_variables():
    file_id = note.create_file_id(
        r"%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s", "", datetime.now()
    )
    assert len(file_id) == 42
    for char in file_id:
        assert char.isdigit()


def test_create_id_with_description():
    file_id = note.create_file_id(
        r"new %h:%m:%s", "# my title\n\n words", datetime.now()
    )
    assert file_id.startswith("new ")
    assert len(file_id) == 12
    for char in file_id[4:]:
        assert char.isdigit() or char == ":"


def test_create_id_with_time_and_uuid():
    file_id = note.create_file_id(
        r"%Y%M%D %uuid4", "# my title\n\n words", datetime.now()
    )
    assert len(file_id) == 45
    for char in file_id[:8]:
        assert char.isdigit()


def test_create_id_with_time_and_title():
    file_id = note.create_file_id(
        r"%Y%M%D %title", "# my title\n\n words", datetime.now()
    )
    assert len(file_id) == 17
    assert file_id.endswith("my title")
    for char in file_id[:8]:
        assert char.isdigit()


########################
#  __create_file_name  #
########################


def test_create_14_digit_file_name():
    file_name = note.__create_file_name(
        ".md", r"%Y%M%D%h%m%s", r"%id", "", datetime.now()
    )
    assert file_name.endswith(".md")
    assert len(file_name) == 17
    for char in file_name[:14]:
        assert char.isdigit()


def test_create_12_digit_text_file_name():
    file_name = note.__create_file_name(
        ".txt", r"%Y%M%D%h%m", r"%id", "", datetime.now()
    )
    assert len(file_name) == 16
    assert file_name.endswith(".txt")
    for char in file_name[:12]:
        assert char.isdigit()


def test_create_file_name_with_no_variables():
    file_name = note.__create_file_name(
        ".md", r"%Y%M%D%h%m%s", r"new file", "", datetime.now()
    )
    assert file_name == "new file.md"


def test_create_file_name_with_custom_format():
    file_name = note.__create_file_name(
        ".md", r"%Y%M%D%h%m%s", r"new_file %h:%m:%s", "", datetime.now()
    )
    assert file_name.startswith("new_file ")
    for char in file_name[10:-3]:
        assert char.isdigit() or char == ":"


def test_create_file_name_with_duplicate_variables():
    file_name = note.__create_file_name(
        ".markdown", r"%Y%M%D%h%m%s", r"%id %id", "", datetime.now()
    )
    assert len(file_name) == 38
    assert file_name.endswith(".markdown")
    assert file_name[:14] == file_name[15:29]


def test_create_file_name_from_title():
    file_name = note.__create_file_name(
        ".md", r"%Y%M%D%h%m%s", r"%title", "    my title        ", datetime.now()
    )
    assert file_name == "my title.md"


def test_create_file_name_from_header():
    file_name = note.__create_file_name(
        ".md", r"%Y%M%D%h%m%s", r"%title", "first line\n# second line", datetime.now()
    )
    assert file_name == "second line.md"


#######################
#  create_file_names  #
#######################


def test_create_file_names_with_no_variables():
    file_names = note.create_file_names(".md", "", r"", ["new file contents"] * 3)
    assert len(file_names) == 3
    for file_name in file_names:
        assert len(file_name) == 33


def test_create_file_names_with_14_digit_id():
    file_names = note.create_file_names(
        ".md", "", r"%Y%M%D%h%m%s", ["new file contents"] * 3
    )
    for file_name in file_names:
        assert len(file_name) == 17
        assert file_name.endswith(".md")
        for char in file_name[:14]:
            assert char.isdigit()
    assert len(set(file_names)) == 3


def test_create_file_names_from_headers():
    file_names = note.create_file_names(
        ".markdown", "", "%title", ["# file one", "# file two", "# file three"]
    )
    assert file_names == [
        "file one.markdown",
        "file two.markdown",
        "file three.markdown",
    ]


def test_create_file_names_from_titles():
    file_names = note.create_file_names(
        ".txt", "", "%title", ["#   file   one", "file two ", "file three\n## here"]
    )
    assert file_names == ["file   one.txt", "file two.txt", "here.txt"]


def test_create_file_names_with_uuids():
    file_names = note.create_file_names(
        ".txt", "", r"%uuid4", ["#   file   one", "file two ", "file three\n## here"]
    )
    for file_name in file_names:
        assert len(file_name) == 34
    assert len(set(file_names)) == 3


###############
#  get_title  #
###############


def test_get_title_from_header():
    assert note.get_title("# my title\n\n words") == "my title"


def test_get_title_from_header_on_second_line():
    assert note.get_title("blah blah \n##  h2 ") == "h2"


def test_get_title_from_line():
    assert note.get_title("my title") == "my title"


def test_get_title_from_no_header():
    assert note.get_title("my title\n\n words") == "my title"


def test_get_title_from_empty_string():
    # An empty file's title is a uuid4.
    assert len(note.get_title("")) == 36


def test_get_title_from_line_after_tag():
    assert note.get_title("#tag\n# 28827 \n asjdlfkd") == "28827"


def test_get_title_from_line_after_fake_title():
    # The line a title is on must not start with any spaces.
    assert note.get_title(" # fake title\n# 28827 \n asjdlfkd") == "28827"


########################
#  validate_file_name  #
########################


def test_validate_file_name_with_valid_name():
    name = "valid_name.txt"
    assert name == note.validate_file_name(name)


def test_validate_file_name_with_invalid_character():
    name = "inv@lid_name.txt"
    assert "inv-lid_name.txt" == note.validate_file_name(name)


def test_validate_file_name_with_invalid_start_and_end():
    name = "-invalid_name  .txt"
    assert "invalid_name.txt" == note.validate_file_name(name)


####################
#  get_file_paths  #
####################


def test_get_file_paths_with_one_path():
    note_content = "[](empty-file.md)"
    note_folder_path = os.path.join(os.getcwd(), "src/tests/assets")
    assert os.path.exists(os.path.join(note_folder_path, "empty-file.md"))
    file_paths = note.get_file_paths(note_content, note_folder_path)
    assert file_paths[0][0] == "empty-file.md"
    path1 = os.path.normpath(os.path.join(note_folder_path, "empty-file.md")).replace(
        "\\", "/"
    )
    assert file_paths[0][1] == path1


def test_get_file_paths_with_only_nonexistent_path():
    note_content = "[](not-a-real-file.md)"
    note_folder_path = os.path.join(os.getcwd(), "src/tests/assets")
    file_paths = note.get_file_paths(note_content, note_folder_path)
    assert len(file_paths) == 0


def test_get_file_paths_with_no_paths():
    note_content = "ajsldfjsdlkjfdslfjlfkfsjk"
    note_folder_path = os.path.join(os.getcwd(), "tests/assets")
    file_paths = note.get_file_paths(note_content, note_folder_path)
    assert len(file_paths) == 0


def test_get_file_paths_with_two_paths():
    note_content = "[](empty-file.md)\n[hi](small-file.md)"
    note_folder_path = os.path.join(os.getcwd(), "src/tests/assets")
    file_paths = note.get_file_paths(note_content, note_folder_path)
    assert len(file_paths) == 2
    assert file_paths[0][0] == "empty-file.md"
    path1 = os.path.normpath(os.path.join(note_folder_path, "empty-file.md")).replace(
        "\\", "/"
    )
    assert file_paths[0][1] == path1
    assert file_paths[1][0] == "small-file.md"
    path2 = os.path.normpath(os.path.join(note_folder_path, "small-file.md")).replace(
        "\\", "/"
    )
    assert file_paths[1][1] == path2


##############################
#  make_file_paths_absolute  #
##############################


def test_make_file_paths_absolute():
    note_content = "[](empty-file.md)"
    cwd = os.getcwd()
    note_path = os.path.normpath(
        os.path.join(cwd, "src/tests/assets/empty-file.md")
    ).replace("\\", "/")
    expected_result = f"[]({note_path})"
    assert expected_result == note.make_file_paths_absolute(note_content, note_path)


def test_make_file_paths_absolute_with_dots():
    note_content = "[](../empty-file.md)"
    cwd = os.getcwd()
    note_path = os.path.normpath(os.path.join(cwd, "src/tests/assets/folder/a-file.md"))
    expected_result = os.path.normpath(
        os.path.join(cwd, "src/tests/assets/empty-file.md")
    ).replace("\\", "/")
    expected_result = f"[]({expected_result})"
    assert expected_result == note.make_file_paths_absolute(note_content, note_path)


def test_make_file_paths_absolute_with_two_paths():
    path1 = "empty-image.png"
    path2 = "small-file.md"
    note_content = f"![]({path1})\n[hi]({path2})"
    cwd = os.getcwd()
    path1 = os.path.normpath(
        os.path.join(cwd, "src/tests/assets/empty-image.png")
    ).replace("\\", "/")
    path2 = os.path.normpath(
        os.path.join(cwd, "src/tests/assets/small-file.md")
    ).replace("\\", "/")
    note_path = os.path.normpath(
        os.path.join(cwd, "src/tests/assets/empty-file.md")
    ).replace("\\", "/")
    expected_result = f"![]({path1})\n[hi]({path2})"
    assert expected_result == note.make_file_paths_absolute(note_content, note_path)


################################
#  __change_all_links_to_file  #
################################


def test___change_all_links_to_file():
    pass

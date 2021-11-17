from datetime import datetime
from note_splitter import note
from note_splitter import settings


####################
#  create_file_id  #
####################


def test_create_14_digit_id():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_id = note.create_file_id('', datetime.now())
    assert len(file_id) == 14
    for char in file_id:
        assert char.isdigit()


def test_create_12_digit_id():
    settings.file_id_format = r'%Y%M%D%h%m'
    file_id = note.create_file_id('# sample title', datetime.now())
    assert len(file_id) == 12
    for char in file_id:
        assert char.isdigit()


def test_create_uuid():
    settings.file_id_format = r'%uuid4'
    file_id = note.create_file_id('## hey', datetime.now())
    assert len(file_id) == 36
    for char in file_id:
        assert char.isalnum() or char == '-'


def test_create_id_from_header():
    settings.file_id_format = r'%title'
    file_id = note.create_file_id('# this is a title', datetime.now())
    assert file_id == 'this is a title'


def test_create_id_from_header_2():
    settings.file_id_format = r'%title'
    file_id = note.create_file_id('##   a title  ', datetime.now())
    assert file_id == 'a title'


def test_create_id_from_lower_header():
    settings.file_id_format = r'%title'
    file_id = note.create_file_id('here is a line of text' \
                                  '\n### title on second line',
                                  datetime.now())
    assert file_id == 'title on second line'


def test_create_id_from_line():
    settings.file_id_format = r'%title'
    file_id = note.create_file_id('line of text\nanother line', datetime.now())
    assert file_id == 'line of text'


def test_create_id_from_custom_format():
    settings.file_id_format = r'%Y-%M-%D_%h:%m:%s'
    file_id = note.create_file_id('', datetime.now())
    assert len(file_id) == 19
    for char in file_id:
        assert char.isdigit() or char in ('-', '_', ':')


def test_create_id_from_duplicate_variables():
    settings.file_id_format = r'%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s'
    file_id = note.create_file_id('', datetime.now())
    assert len(file_id) == 42
    for char in file_id:
        assert char.isdigit()


def test_create_id_with_description():
    settings.file_id_format = r'new %h:%m:%s'
    file_id = note.create_file_id('# my title\n\n words', datetime.now())
    assert file_id.startswith('new ')
    assert len(file_id) == 12
    for char in file_id[4:]:
        assert char.isdigit() or char == ':'


def test_create_id_with_time_and_uuid():
    settings.file_id_format = r'%Y%M%D %uuid4'
    file_id = note.create_file_id('# my title\n\n words', datetime.now())
    assert len(file_id) == 45
    for char in file_id[:8]:
        assert char.isdigit()


def test_create_id_with_time_and_title():
    settings.file_id_format = r'%Y%M%D %title'
    file_id = note.create_file_id('# my title\n\n words', datetime.now())
    assert len(file_id) == 17
    assert file_id.endswith('my title')
    for char in file_id[:8]:
        assert char.isdigit()


########################
#  __create_file_name  #
########################


def test_create_14_digit_file_name():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_name = note.__create_file_name('.md', r'%id', '', datetime.now())
    assert file_name.endswith('.md')
    assert len(file_name) == 17
    for char in file_name[:14]:
        assert char.isdigit()


def test_create_12_digit_text_file_name():
    settings.file_id_format = r'%Y%M%D%h%m'
    file_name = note.__create_file_name('.txt', r'%id', '', datetime.now())
    assert len(file_name) == 16
    assert file_name.endswith('.txt')
    for char in file_name[:12]:
        assert char.isdigit()


def test_create_file_name_with_no_variables():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_name = note.__create_file_name('.md', r'new file', '', datetime.now())
    assert file_name == 'new file.md'


def test_create_file_name_with_custom_format():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_name = note.__create_file_name('.md',
                                        r'new_file %h:%m:%s',
                                        '',
                                        datetime.now())
    assert file_name.startswith('new_file ')
    for char in file_name[10:-3]:
        assert char.isdigit() or char == ':'


def test_create_file_name_with_duplicate_variables():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_name = note.__create_file_name('.markdown',
                                        r'%id %id',
                                        '',
                                        datetime.now())
    assert len(file_name) == 38
    assert file_name.endswith('.markdown')
    assert file_name[:14] == file_name[15:29]


def test_create_file_name_from_title():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_name = note.__create_file_name('.md',
                                        r'%title',
                                        '    my title        ',
                                        datetime.now())
    assert file_name == 'my title.md'


def test_create_file_name_from_header():
    settings.file_id_format = r'%Y%M%D%h%m%s'
    file_name = note.__create_file_name('.md',
                                        r'%title',
                                        'first line\n# second line',
                                        datetime.now())
    assert file_name == 'second line.md'


#######################
#  create_file_names  #
#######################


def test_create_file_names_with_no_variables():
    settings.file_name_format = r''
    file_names = note.create_file_names('.md', ['new file contents'] * 3)
    assert file_names == ['.md'] * 3


def test_create_file_names_with_14_digit_id():
    settings.file_name_format = r'%Y%M%D%h%m%s'
    file_names = note.create_file_names('.md', ['new file contents'] * 3)
    for file_name in file_names:
        assert len(file_name) == 17
        assert file_name.endswith('.md')
        for char in file_name[:14]:
            assert char.isdigit()
    assert len(set(file_names)) == 3


def test_create_file_names_from_headers():
    settings.file_name_format = '%title'
    file_names = note.create_file_names('.markdown', ['# file one',
                                                      '# file two',
                                                      '# file three'])
    assert file_names == ['file one.markdown',
                          'file two.markdown',
                          'file three.markdown']


def test_create_file_names_from_titles():
    settings.file_name_format = '%title'
    file_names = note.create_file_names('.txt', ['#   file   one',
                                                 'file two ',
                                                 'file three\n## here'])
    assert file_names == ['file   one.txt',
                          'file two.txt',
                          'here.txt']


def test_create_file_names_with_uuids():
    settings.file_name_format = r'%uuid4'
    file_names = note.create_file_names('.txt', ['#   file   one',
                                                 'file two ',
                                                 'file three\n## here'])
    for file_name in file_names:
        assert len(file_name) == 40
    assert len(set(file_names)) == 3


###############
#  get_title  #
###############


def test_get_title_from_header():
    assert note.get_title('# my title\n\n words') == 'my title'


def test_get_title_from_header_on_second_line():
    assert note.get_title('blah blah \n##  h2 ') == 'h2'


def test_get_title_from_line():
    assert note.get_title('my title') == 'my title'


def test_get_title_from_no_header():
    assert note.get_title('my title\n\n words') == 'my title'


def test_get_title_from_empty_string():
    assert note.get_title('') == ''


def test_get_title_from_line_after_tag():
    assert note.get_title('#tag\n# 28827 \n asjdlfkd') == '28827'


def test_get_title_from_line_after_fake_title():
    # The line a title is on must not start with any spaces.
    assert note.get_title(' # fake title\n# 28827 \n asjdlfkd') == '28827'

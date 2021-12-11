"""The user's application settings.

Some of these settings may be hidden from the user.

The settings for the formats of file names and IDs can use the following
variables:

 * ``%uuid4`` - A universally unique identifier.
 * ``%title`` - The title of the file (the body of its first header, or 
   the first line of the file if there is no header).
 * ``%Y`` - The current year.
 * ``%M`` - The current month.
 * ``%D`` - The current day.
 * ``%h`` - The current hour.
 * ``%m`` - The current minute.
 * ``%s`` - The current second.

Additionally, the file name format setting can use the ``%id`` variable,
which gets replaced with the ID of the file as described by the file ID 
format setting.

Every time file_id_format is changed, file_id_regex must be updated.

Attributes
----------
backlink: bool
    Whether or not to append a backlink to the source file in each new 
    file.
copy_frontmatter : bool
    Whether or not to copy frontmatter from the source file to each new 
    file.
copy_global_tags : bool
    Whether or not to copy global tags from the source file to each new 
    file.
parse_blocks : bool
    Whether or not to create ``Block`` tokens while parsing.
create_index_file : bool
    Whether or not to create an index file.
destination_folder_path : str
    The absolute path to the user's folder where new files will be 
    saved.
file_id_format : str
    The format of the file IDs.
file_id_regex : str
    The uncompiled regular expression to use to extract file IDs from 
    the files.
file_name_format : str
    The format of the new file names.
note_types : List[str]
    The file extensions of the files that may be chosen to be split.Each
    must start with a period.
replace_split_contents : bool
    Whether or not to replace the parts of the source file that was 
    split out with links to the new files.
source_folder_path : str
    The absolute path to the user's folder containing the files to be 
    split.
split_attrs : dict
    The attributes to split by. If the chosen split type has an 
    attribute, it can be used to narrow down what to split by.
split_keyword : str
    The tag/keyword the program searches for to know which file(s) to 
    split.
split_type : Type
    The type to split by. This can be any token type, even an abstract 
    one.
"""
# This module follows the Global Object Pattern. You can see more 
# details about this design pattern here: 
# https://python-patterns.guide/python/module-globals/#id1


from typing import List, Type, Callable
import sqlite3
import json 
from note_splitter import tokens


backlink: bool = True
copy_frontmatter: bool = True
copy_global_tags: bool = True
parse_blocks: bool = True
create_index_file: bool = True
destination_folder_path: str = ''
file_id_format: str = r'%Y%M%D%h%m%s'
file_id_regex: str = r'\d{14}'
file_name_format: str = r'%id'
note_types: List[str] = [".md", ".markdown", ".txt"]
replace_split_contents: bool = False
source_folder_path: str = ''
split_attrs: dict = {'level': 2}
split_keyword: str = '#split'
split_type: Type = tokens.Header


def initialize():
    """Initialize the settings with default values"""
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute('''
        CREATE TABLE settings
            (split_keyword TEXT,
            source_folder_path TEXT,
            destination_folder_path TEXT,
            note_types TEXT,
            split_type TEXT,
            split_attrs TEXT,
            file_name_format TEXT,
            file_id_format TEXT,
            file_id_regex TEXT,
            parse_blocks INTEGER,
            copy_frontmatter INTEGER,
            copy_global_tags INTEGER,
            backlink INTEGER,
            create_index_file INTEGER,
            replace_split_contents INTEGER)''')
    cur.execute("""
        INSERT INTO settings
            (split_keyword,
            source_folder_path,
            destination_folder_path,
            note_types,
            split_type,
            split_attrs,
            file_name_format,
            file_id_format,
            file_id_regex,
            parse_blocks,
            copy_frontmatter,
            copy_global_tags,
            backlink,
            create_index_file,
            replace_split_contents)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (split_keyword,
        source_folder_path,
        destination_folder_path,
        ','.join(note_types),
        get_token_type_name(split_type),
        json.dumps(split_attrs),
        file_name_format,
        file_id_format,
        file_id_regex,
        int(parse_blocks),
        int(copy_frontmatter),
        int(copy_global_tags),
        int(backlink),
        int(create_index_file),
        int(replace_split_contents)))

    connection.commit()
    connection.close()


def load() -> None:
    """Fetch the current user settings from the database"""
    connection = sqlite3.connect('store-transactions.db')
    cur = connection.cursor()
    try:
        cur.execute('SELECT * from settings')
    except sqlite3.OperationalError:
        initialize()
    else:
        result = cur.fetchall()

        global split_keyword
        global source_folder_path
        global destination_folder_path
        global note_types
        global split_type
        global split_attrs
        global file_name_format
        global file_id_format
        global file_id_regex
        global parse_blocks
        global copy_frontmatter
        global copy_global_tags
        global backlink
        global create_index_file
        global replace_split_contents

        split_keyword = str(result[0][0])
        source_folder_path = str(result[0][1])
        destination_folder_path = str(result[0][2])
        note_types = result[0][3].split(',')
        split_type = get_token_type(result[0][4])
        split_attrs = json.loads(result[0][5])
        file_name_format = str(result[0][6])
        file_id_format = str(result[0][7])
        file_id_regex = str(result[0][8])
        parse_blocks = bool(result[0][9])
        copy_frontmatter = bool(result[0][10])
        copy_global_tags = bool(result[0][11])
        backlink = bool(result[0][12])
        create_index_file = bool(result[0][13])
        replace_split_contents = bool(result[0][14])
    
    connection.commit()
    connection.close()


def drop_table() -> None:
    """Delete the user settings database."""
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    try:
        cur.execute('DROP TABLE settings')
    except sqlite3.OperationalError:
        pass
    else:
        connection.commit()
        connection.close()


def save() -> None:
    """Saves the user's settings to the database."""
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("""
        UPDATE settings
        SET split_keyword = ?,
            source_folder_path = ?,
            destination_folder_path = ?,
            note_types = ?,
            split_type = ?,
            split_attrs = ?,
            file_name_format = ?,
            file_id_format = ?,
            file_id_regex = ?,
            parse_blocks = ?,
            copy_frontmatter = ?,
            copy_global_tags = ?,
            backlink = ?,
            create_index_file = ?,
            replace_split_contents = ?""",
        (split_keyword,
        source_folder_path,
        destination_folder_path,
        ','.join(note_types),
        get_token_type_name(split_type),
        json.dumps(split_attrs),
        file_name_format,
        file_id_format,
        file_id_regex,
        int(parse_blocks),
        int(copy_frontmatter),
        int(copy_global_tags),
        int(backlink),
        int(create_index_file),
        int(replace_split_contents)))
    connection.commit()
    connection.close()


def reset() -> None:
    """Reset current settings to default"""
    drop_table()
    initialize()


def get_token_type_names(
        filter_predicate: Callable[[Type], bool] = None,
        all_token_types: List[Type] = None) -> List[str]:
    """Get all token types' output-formatted names.
    
    Parameters
    ----------
    predicate : Callable, optional
        A function that filters the token types.
    all_token_types : List, optional
        A list of all token types. If not provided, the list of all 
        token types will be fetched.
    """
    if not all_token_types:
        all_token_types: List[Type] = tokens.get_all_token_types(tokens)
    token_names = []
    for token_type in all_token_types:
        if not filter_predicate or filter_predicate(token_type):
            token_names.append(get_token_type_name(token_type))
    return token_names


def get_token_type_name(token_type: Type) -> str:
    """Get the token type's output-formatted name.
    
    Parameters
    ----------
    token_type : Type
        The token type to get the name of.
    """
    token_name = ''
    for i, letter in enumerate(token_type.__name__):
        if i and letter.isupper():
            token_name += ' '
        token_name += letter
    return token_name.lower()


def get_token_type(chosen_name: str) -> Type:
    """Get a token type by name.
    
    Parameters
    ----------
    chosen_name : str
        The output-formatted name of the token type to get.
    """
    all_token_types: List[Type] = tokens.get_all_token_types(tokens)
    token_type_names = get_token_type_names(None, all_token_types)
    for name, type_ in zip(token_type_names, all_token_types):
        if name == chosen_name:
            return type_
    raise ValueError(f'Token type "{chosen_name}" not found.')

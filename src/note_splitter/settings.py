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


from typing import List, Type
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


def initialize_settings():
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


def get_current_settings() -> None:
    """Fetch the current user settings from the database"""
    connection = sqlite3.connect('store-transactions.db')
    cur = connection.cursor()
    try:
        cur.execute('SELECT * from settings')
    except sqlite3.OperationalError:
        initialize_settings()
    else:
        result = cur.fetchall()
        # TODO: put the settings from result into the other variables.


def delete_current_settings() -> None:
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


def insert_settings_to_db(cur, connection) -> None:
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


def save_settings_to_db() -> None:
    """Update the user settings in the database"""
    delete_current_settings()
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    try:
        insert_settings_to_db(cur, connection)
    except sqlite3.OperationalError:
        initialize_settings()
        insert_settings_to_db(cur, connection)
    finally:
        connection.commit()
        connection.close()


def reset_settings_to_default() -> None:
    """Reset current settings to default"""
    delete_current_settings()
    initialize_settings()


def get_all_token_type_names() -> List[str]:
    """Get all token type names."""
    all_token_types: List[Type] = tokens.get_all_token_types(tokens)
    token_names = []
    for token_type in all_token_types:
        token_names.append(get_token_type_name(token_type))
    return token_names


def get_token_type_name(token_type: Type) -> str:
    """Get the token type name.
    
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


def get_token_type(name: str) -> Type:
    """Get a token type by name."""
    # TODO

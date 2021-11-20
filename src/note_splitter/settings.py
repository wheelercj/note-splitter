"""The user's application settings.

Some of these settings may be hidden from the user.

Attributes
----------
split_keyword : str
    The tag/keyword the program searches for to know which file(s) 
    to split.
source_folder_path : str
    The absolute path to the user's folder containing the files to 
    be split.
destination_folder_path : str
    The absolute path to the user's folder where new files will be 
    saved.
note_types : List[str]
    The file extensions of the files that may be chosen to be split.
    Each must start with a period.
create_blocks: bool
    Whether or not to create ``Block`` tokens while parsing.
copy_frontmatter: bool
    Whether or not to copy frontmatter from the source file to each 
    new file.
copy_global_tags: bool
    Whether or not to copy global tags from the source file to each 
    new file.
split_type: Type
    The type to split by. This can be any token type, even an abstract 
    one.
split_attrs: dict
    The attributes to split by. If the chosen split type has an 
    attribute, it can be used to narrow down what to split by.
new_file_name_format: str
    The format of the new file names. # TODO: figure out exactly what 
    formats this string should be able to have. Maybe do the same thing
    as zettlr: https://docs.zettlr.com/en/reference/settings/#advanced
backlink: bool
    Whether or not to append a backlink to the source file in each new 
    file.
create_index_file: bool
    Whether or not to create an index file.
replace_split_contents: bool
    Whether or not to replace the parts of the source file that was
    split out with links to the new files.
"""
# This module follows the Global Object Pattern. You can see more 
# details about this design pattern here: 
# https://python-patterns.guide/python/module-globals/#id1


from typing import List, Type
import sqlite3
import os
import json 
from note_splitter import tokens

split_keyword: str = '#split'
source_folder_path: str = os.path.abspath(os.curdir)
destination_folder_path: str = ''
note_types: List[str] = [".md", ".markdown", ".txt"]
split_type: Type = tokens.Header
split_attrs: dict = dict()
new_file_name_format: str = r'%id'
file_id_format: str = r'%Y%M%D%h%m%s'
file_id_regex: str = r'\d{14}'
create_blocks: bool = True
copy_frontmatter: bool = True
copy_global_tags: bool = True
backlink: bool = True
create_index_file: bool = True
replace_split_contents: bool = False

def initialize_settings():
    """Initialize the settings with default values"""
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute('''CREATE TABLE settings (split_keyword text, source_folder_path text, destination_folder_path text,  
                note_types text, split_type text, split_attrs text, new_file_name_format text, file_id_format text, file_id_regex text, create_blocks integer, 
                copy_frontmatter integer, copy_global_tags integer, backlink integer, create_index_file integer, replace_split_contents integer)''')
    cur.execute("""INSERT INTO settings  (split_keyword, source_folder_path, destination_folder_path,  
                note_types, split_type, split_attrs, new_file_name_format, file_id_format, file_id_regex create_blocks, 
                copy_frontmatter, copy_global_tags, backlink, create_index_file, replace_split_contents) VALUES(?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?)""", (split_keyword, source_folder_path, destination_folder_path, 
                ','.join(note_types), split_type__name__, json.dumps(split_attrs), new_file_name_format, int(create_blocks), int(copy_frontmatter), 
                int(copy_global_tags), int(backlink), int(create_index_file), int(replace_split_contents)))
    connection.commit()
    connection.close()

def get_current_settings():
    """Fetch the current user settings from the database"""
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("SELECT * from settings")
    result = cur.fetchall()
    print(result)

def delete_current_settings():
    """Delete the user settings from the database"""
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("DELETE from settings")
    connection.commit()
    connection.close()

def update_settings():
    """Update the user settings in the database"""
    delete_current_settings()
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("""INSERT INTO settings  (split_keyword, source_folder_path, destination_folder_path,  
                note_types, split_type, split_attrs, new_file_name_format, file_id_format, file_id_regex create_blocks, 
                copy_frontmatter, copy_global_tags, backlink, create_index_file, replace_split_contents) VALUES(?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?)""", (split_keyword, source_folder_path, destination_folder_path, 
                ','.join(note_types), split_type__name__, json.dumps(split_attrs), new_file_name_format, int(create_blocks), int(copy_frontmatter), 
                int(copy_global_tags), int(backlink), int(create_index_file), int(replace_split_contents)))
    connection.commit()
    connection.close()

def reset_settings_to_default():
    """Reset current settings to default"""
    delete_current_settings()
    initialize_settings()
    


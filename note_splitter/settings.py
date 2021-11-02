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
    The format of the new file names. TODO: figure out exactly what 
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
# This module uses the Global Object Pattern. See more details about 
# this design pattern here: 
# https://python-patterns.guide/python/module-globals/#id1


# external imports
from typing import List, Type
import sqlite3
import os

# internal imports
import tokens


split_keyword: str = '#split'
source_folder_path: str = os.path.abspath(os.curdir)
destination_folder_path: str = ''
note_types: str = '.md .markdown .txt'
create_blocks: bool = True
copy_frontmatter: bool = True
copy_global_tags: bool = True
split_type: Type = tokens.Header
split_attrs: dict = dict()
new_file_name_format: str = r'%id.md'
backlink: bool = True
create_index_file: bool = True
replace_split_contents: bool = False


def initialize_settings():
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute('''CREATE TABLE settings (split_keyword text, source_folder_path text, destination_folder_path text, split_header_level real, note_types text)''')
    cur.execute("INSERT INTO settings  (split_keyword, source_folder_path, destination_folder_path, split_header_level, note_types) VALUES(?,?,?,?,?)", (split_keyword, source_folder_path, destination_folder_path, split_header_level, note_types))
    connection.commit()
    connection.close()

def get_current_settings():
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("SELECT * from settings")
    result = cur.fetchall()
    print(result)

def delete_current_settings():
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("DELETE from settings")
    connection.commit()
    connection.close()

def update_settings():
    delete_current_settings()
    connection = sqlite3.connect('store-transactions.db') 
    cur = connection.cursor()
    cur.execute("INSERT INTO settings  (split_keyword, source_folder_path, destination_folder_path, split_header_level, note_types) VALUES(?,?,?,?,?)", (split_keyword, source_folder_path, destination_folder_path, split_header_level, note_types))
    connection.commit()
    connection.close()



    
  






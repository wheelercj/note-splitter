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
split_header_level : int
    The header level to split by.
note_types : List[str]
    The file extensions of the files that may be chosen to be split.
    Each must start with a period.
"""
# This module uses the Global Object Pattern. See more details about 
# this design pattern here: 
# https://python-patterns.guide/python/module-globals/#id1


from typing import List


split_keyword: str = '#split'
source_folder_path: str = ''
destination_folder_path: str = ''
split_header_level: int = 4
note_types: List[str] = ['.md', '.markdown', '.txt']

# external imports
# from typing import List
import os
from datetime import datetime

# internal imports
# from note import Note, get_chosen_notes
import settings
from note import create_time_id_file_names
import tokens
from lexer import Lexer
from parser_ import AST
from splitter import Splitter

def main():
    settings.split_type = tokens.OrderedListItem
    settings.split_attrs = dict()
    
    # notes: List[Note] = get_chosen_notes()
    file_path = input('Enter the absolute path of the file to split by numbered list items:\n')
    with open(file_path, 'r', encoding='utf8') as file:
        content = file.read()
    tokenize = Lexer()
    tokens_ = tokenize(content)
    # ast = AST(tokens_)
    split = Splitter()
    # sections = split(ast.content)
    sections = split(tokens_)
    
    folder_path, _ = os.path.split(file_path)
    new_file_names = create_time_id_file_names('.md', len(sections))

    for i, section in enumerate(sections):
        new_file_name = new_file_names[i]
        new_file_path = os.path.join(folder_path, new_file_name)
        with open(new_file_path, 'x', encoding='utf8') as file:
            file.write(str(section))
    print(f'Created {len(sections)} new files.')


if __name__ == '__main__':
    main()

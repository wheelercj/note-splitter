# external imports
# from typing import List
import os
from datetime import datetime

# internal imports
# from note import Note, get_chosen_notes
import settings
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
    
    now = datetime.now()
    zk_id_now = int(f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}')
    folder_path, _ = os.path.split(file_path)

    for section in sections:
        new_file_name = f'{zk_id_now}.md'
        new_file_path = os.path.join(folder_path, new_file_name)
        zk_id_now += 1
        with open(new_file_path, 'x', encoding='utf8') as file:
            file.write(str(section))
    print(f'Created {len(sections)} new files.')


if __name__ == '__main__':
    main()

"""This module runs the entire application."""


import os
from typing import List, Callable
from note_splitter import settings, tokens
from note_splitter.note import Note, \
                               get_chosen_notes, \
                               create_time_id_file_names
from note_splitter.lexer import Lexer
from note_splitter.parser_ import AST
from note_splitter.splitter import Splitter
from note_splitter.formatter_ import Formatter


def main() -> None:
    """Runs the entire application."""
    tokenize: Callable = Lexer()
    split: Callable = Splitter()
    format_: Callable = Formatter()
    
    notes: List[Note] = get_chosen_notes()
    for note in notes:
        with open(note.path, 'r', encoding='utf8') as file:
            content: str = file.read()
        split_contents: List[str] = split_text(content,
                                               tokenize,
                                               split,
                                               format_)
        new_file_names: List[str] = create_file_names(note.ext,
                                                      len(split_contents))
        save_new_notes(split_contents, new_file_names)
        print(f'Created {len(split_contents)} new files.')


def split_text(content: str,
               tokenize: Callable,
               split: Callable,
               format_: Callable) -> List[str]:
    """Splits a string into multiple strings based on several factors.
    
    Attributes
    ----------
    content: str
        The string to be split.
    tokenize: Callable
        A function created from the Lexer class that converts a string 
        into a list of tokens.
    split: Callable
        A function created from the Splitter class that groups the 
        tokens into sections.
    format_: Callable
        A function created from the Formatter class that adjusts the 
        formatting of each section and converts them to strings.
    """
    tokens_: List[tokens.Token] = tokenize(content)
    ast = AST(tokens_, settings.create_blocks)
    sections: List[tokens.Section] = split(ast.content,
                                            settings.split_type,
                                            settings.split_attrs)
    split_contents: List[str] = format_(sections,
                                        ast.global_tags,
                                        ast.frontmatter)
    return split_contents


def create_file_names(note_ext: str, note_count: int) -> List[str]:
    """Creates the names for all the new files.
    
    Parameters
    ----------
    note_ext: str
        The extension of the files to be created.
    note_count: int
        The number of files to be created.
    """
    if settings.new_file_name_format == r'%id':
        return create_time_id_file_names(note_ext, note_count)
    else:
        raise ValueError('Invalid value in ' \
                        f'{settings.new_file_name_format.__name__}')


def save_new_notes(split_contents: List[str], new_file_names: List[str]):
    """Creates new files and saves strings into them.
    
    The lists for the contents and names of the new files are parallel.

    Attributes
    ----------
    split_contents: List[str]
        A list of strings to each be saved into a new file.
    new_file_names: List[str]
        A list of names of files to be created.
    """
    for i, split_content in enumerate(split_contents):
        new_file_name = os.path.join(settings.new_notes_folder,
                                     new_file_names[i])
        with open(new_file_name, 'x', encoding='utf8') as file:
            file.write(split_content)


if __name__ == '__main__':
    main()

"""This module runs the entire application."""


import os
import uuid
from typing import List, Callable
from note_splitter import settings, tokens
from note_splitter import note
from note_splitter.lexer import Lexer
from note_splitter.parser_ import AST
from note_splitter.splitter import Splitter
from note_splitter.formatter_ import Formatter


def main() -> None:
    """Runs the entire application."""
    tokenize: Callable = Lexer()
    split: Callable = Splitter()
    format_: Callable = Formatter()
    
    notes: List[note.Note] = note.get_chosen_notes()
    for n in notes:
        with open(n.path, 'r', encoding='utf8') as file:
            content: str = file.read()
        split_contents: List[str] = split_text(content,
                                               tokenize,
                                               split,
                                               format_)
        new_file_names: List[str] = note.create_file_names(n.ext,
                                                           split_contents)
        new_notes = save_new_notes(split_contents, new_file_names)
        print(f'Created {len(new_notes)} new files.')
        index_path = create_index_file(new_notes, new_notes[0].folder_path)
        print(f'Created index file at {index_path}')


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


def save_new_notes(split_contents: List[str],
                   new_file_names: List[str]) -> List[note.Note]:
    """Creates new files and saves strings into them.
    
    The lists for the contents and names of the new files are parallel.

    Attributes
    ----------
    split_contents: List[str]
        A list of strings to each be saved into a new file.
    new_file_names: List[str]
        A list of names of files to be created.

    Returns
    -------
    new_notes: List[note.Note]
        The newly created notes.
    """
    new_notes = []
    for new_file_name, split_content in zip(new_file_names, split_contents):
        new_file_path = os.path.join(settings.new_notes_folder, new_file_name)
        with open(new_file_path, 'x', encoding='utf8') as file:
            file.write(split_content)
        new_notes.append(note.Note(new_file_path))
    
    return new_notes


def create_index_file(new_notes: List[note.Note], folder_path: str) -> str:
    """Creates an index file for the new notes.
    
    Parameters
    ----------
    new_notes: List[note.Note]
        The newly created notes.

    Returns
    -------
    index_file_path: str
        The path to the newly created index file.
    """
    unique_string = uuid.uuid4().hex[:10]
    index_file_path = os.path.join(folder_path, f'index {unique_string}.md')
    with open(index_file_path, 'x', encoding='utf8') as file:
        file.write('# index\n\n')
        for note in new_notes:
            file.write(f'* [{note.title}]({note.path})\n')

    return index_file_path


if __name__ == '__main__':
    main()

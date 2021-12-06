"""This module runs the entire application."""


import os
from typing import List, Callable
import PySimpleGUI as sg  # https://pysimplegui.readthedocs.io/en/latest/
from note_splitter import settings, tokens, note, gui
from note_splitter.lexer import Lexer
from note_splitter.parser_ import AST
from note_splitter.splitter import Splitter
from note_splitter.formatter_ import Formatter


def run_main_menu() -> None:
    """Displays the main menu."""
    sg.theme('TanBlue')
    window = gui.create_main_menu_window()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            window.close()
            return
        gui.handle_main_menu_event(event, values, window)


def show_progress(note_number: int,
                  note_count: int,
                  call_number: int,
                  call_count: int) -> None:
    """Shows the progress of the application.

    Parameters
    ----------
    note_number: int
        The number of the note being processed.
    note_count: int
        The total number of notes being processed.
    call_number: int
        The number of the call to this function.
    call_count: int
        The total number of calls to this function.
    """
    n = int((note_number + call_number) / (note_count * call_count) * 100)
    sg.one_line_progress_meter('Splitting', n, 100, '-PROGRESS_METER-')


def split_files(notes: List[note.Note] = None) -> None:
    """Splits files into multiple smaller files.
    
    If no notes are provided, they will be found using the split keyword
    and the source folder path chosen in settings.

    Parameters
    ----------
    notes: List[note.Note]
        The notes to be split.
    """
    tokenize: Callable = Lexer()
    split: Callable = Splitter()
    format_: Callable = Formatter()
    
    if notes is None:
        notes: List[note.Note] = note.get_chosen_notes()
    for i, source_note in enumerate(notes):
        show_progress(i, len(notes), 1, 5)
        with open(source_note.path, 'r', encoding='utf8') as file:
            content: str = file.read()
        show_progress(i, len(notes), 2, 5)
        split_contents: List[str] = split_text(content,
                                               tokenize,
                                               split,
                                               format_)
        show_progress(i, len(notes), 3, 5)
        new_file_names: List[str] = note.create_file_names(source_note.ext,
                                                           split_contents)
        show_progress(i, len(notes), 4, 5)
        new_notes = save_new_notes(split_contents, new_file_names)
        show_progress(i, len(notes), 5, 5)
        print(f'Created {len(new_notes)} new files.')
        if settings.create_index_file:
            index_path = create_index_file_(source_note, new_notes)
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
        new_file_path = note.ensure_file_path_uniqueness(new_file_path)
        with open(new_file_path, 'x', encoding='utf8') as file:
            file.write(split_content)
        new_notes.append(note.Note(new_file_path))
    return new_notes


def create_index_file_(source_note: note.Note,
                       new_notes: List[note.Note]) -> str:
    """Creates an index file for the new notes in the same folder.
    
    Parameters
    ----------
    source_note: note.Note
        The note that the new notes were created from.
    new_notes: List[note.Note]
        The newly created notes.

    Returns
    -------
    index_file_path: str
        The absolute path to the newly created index file.
    """
    index_name = note.validate_file_name(f'index - {source_note.title}.md', 35)
    index_file_path = os.path.join(new_notes[0].folder_path, index_name)
    index_file_path = note.ensure_file_path_uniqueness(index_file_path)
    with open(index_file_path, 'x', encoding='utf8') as file:
        file.write(f'# index of {source_note.title}\n\n')
        for n in new_notes:
            file.write(f'* [{n.title}]({n.path})\n')
    return index_file_path


if __name__ == '__main__':
    run_main_menu()

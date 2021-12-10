"""This module runs the entire application."""


import os
from tkinter import filedialog
from typing import List, Tuple, Callable
import webbrowser
import PySimpleGUI as sg  # https://pysimplegui.readthedocs.io/en/latest/
from note_splitter import settings, tokens, note, gui
from note_splitter.lexer import Lexer
from note_splitter.parser_ import AST
from note_splitter.splitter import Splitter
from note_splitter.formatter_ import Formatter


def run_main_menu() -> None:
    """Displays the main menu."""
    sg.theme('TanBlue')
    settings.get_current_settings()
    window = gui.create_main_menu_window()
    listbox_notes: List[note.Note] = []
    all_notes: List[note.Note] = []
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            settings.save_settings_to_db()
            window.close()
            return
        listbox_notes, all_notes = handle_main_menu_event(event,
                                                          values,
                                                          window,
                                                          listbox_notes,
                                                          all_notes)


def split_files(window: sg.Window,
                notes: List[note.Note] = None) -> List[note.Note]:
    """Splits files into multiple smaller files.
    
    If no notes are provided, they will be found using the split keyword
    and the source folder path chosen in settings.

    Parameters
    ----------
    window : sg.Window
        The main menu window.
    notes : List[note.Note]
        The notes to be split.

    Returns
    -------
    new_notes : List[note.Note]
        The newly created notes.
    """
    tokenize: Callable = Lexer()
    split: Callable = Splitter()
    format_: Callable = Formatter()
    
    if not notes:
        notes: List[note.Note] = note.get_chosen_notes(window)
    all_new_notes: List[note.Note] = []
    for i, source_note in enumerate(notes):
        gui.show_progress(i, len(notes), 1, 5)
        with open(source_note.path, 'r', encoding='utf8') as file:
            content: str = file.read()
        gui.show_progress(i, len(notes), 2, 5)
        split_contents: List[str] = split_text(content,
                                               tokenize,
                                               split,
                                               format_)
        gui.show_progress(i, len(notes), 3, 5)
        new_file_names: List[str] = note.create_file_names(source_note.ext,
                                                           split_contents)
        gui.show_progress(i, len(notes), 4, 5)
        new_notes = save_new_notes(split_contents, new_file_names)
        all_new_notes.extend(new_notes)
        gui.show_progress(i, len(notes), 5, 5)
        print(f'Created {len(new_notes)} new files.')
        if settings.create_index_file:
            index_path = create_index_file_(source_note, new_notes)
            print(f'Created index file at {index_path}')
            all_new_notes.append(note.Note(index_path))

    return all_new_notes


def split_text(content: str,
               tokenize: Callable,
               split: Callable,
               format_: Callable) -> List[str]:
    """Splits a string into multiple strings based on several factors.
    
    Attributes
    ----------
    content : str
        The string to be split.
    tokenize : Callable
        A function created from the Lexer class that converts a string 
        into a list of tokens.
    split : Callable
        A function created from the Splitter class that groups the 
        tokens into sections.
    format_ : Callable
        A function created from the Formatter class that adjusts the 
        formatting of each section and converts them to strings.

    Returns
    -------
    split_contents : List[str]
        A list of strings that are the sections of the original string.
    """
    tokens_: List[tokens.Token] = tokenize(content)
    ast = AST(tokens_, settings.parse_blocks)
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
    split_contents : List[str]
        A list of strings to each be saved into a new file.
    new_file_names : List[str]
        A list of names of files to be created.

    Returns
    -------
    new_notes : List[note.Note]
        The newly created notes.
    """
    new_notes = []
    for new_file_name, split_content in zip(new_file_names, split_contents):
        if not settings.destination_folder_path:
            settings.destination_folder_path = \
                note.require_folder_path('destination')
        new_file_path = os.path.join(settings.destination_folder_path,
                                     new_file_name)
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
    source_note : note.Note
        The note that the new notes were created from.
    new_notes : List[note.Note]
        The newly created notes.

    Returns
    -------
    index_file_path : str
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


def handle_main_menu_event(
        event,
        values,
        window,
        listbox_notes: List[note.Note],
        all_notes: List[note.Note]) -> List[note.Note]:
    """Handles the main menu's events.
    
    Parameters
    ----------
    event : tkinter.Event
        The event that occurred.
    values : dict
        The values of the widgets in the main menu.
    window : tkinter.Tk
        The main menu window.
    listbox_notes : List[note.Note]
        The notes displayed in the listbox. This list may be empty.
    all_notes : List[note.Note]
        All of the user's notes. This list may be empty.

    Returns
    -------
    listbox_notes : List[note.Note]
        The notes displayed in the listbox. This list may be empty.
    all_notes : List[note.Note]
        All of the user's notes. This list may be empty.
    """
    if event == 'Tips':
        sg.popup('Visit each of the tabs to see available applications.',
                 'Various tabs are included such as development environment ' \
                 'setup, Note Splitter overview, token hierarchy, program ' \
                 'modules, references, and how the documentation is ' \
                 'maintained.',
                 'If you have any questions or concerns please message the ' \
                 'developers on the GitHub page.', keep_on_top=True)
    elif event.startswith('URL '):
        url = event.split(' ')[1]
        webbrowser.open(url)
    elif event == 'Open File':
        all_notes = note.get_all_notes(window)
        file_paths: Tuple[str] = filedialog.askopenfilenames()
        listbox_notes: List[note.Note] = [note.Note(f) for f in file_paths]
        titles: List[str] = [n.title for n in listbox_notes]
        window['-NOTES TO SPLIT-'].update(values=titles)
    elif event == 'find':
        all_notes = note.get_all_notes(window)
        listbox_notes: List[note.Note] = note.get_chosen_notes(window,
                                                               all_notes)
        titles: List[str] = [n.title for n in listbox_notes]
        window['-NOTES TO SPLIT-'].update(values=titles)
    elif event == 'Split all':
        new_notes: List[note.Note] = split_files(window, listbox_notes)
        gui.run_split_summary_window(new_notes, all_notes)
        window['-NOTES TO SPLIT-'].update(values=[])
    elif event == 'Split selected':
        notes_to_split = [note.get_by_title(listbox_notes, title)
                          for title in values['-NOTES TO SPLIT-']]
        if not notes_to_split:
            sg.popup('No notes selected.', keep_on_top=True)
        else:
            new_notes: List[note.Note] = split_files(window, notes_to_split)
            gui.run_split_summary_window(new_notes, all_notes)
            listbox_notes = [n for n in listbox_notes 
                             if n.title not in values['-NOTES TO SPLIT-']]
            titles = [n.title for n in listbox_notes]
            window['-NOTES TO SPLIT-'].update(values=titles)
    elif event == 'parseBlocks':
        gui.update_split_types(values, window)
    elif event == '-SPLIT TYPE-':
        settings.split_type = settings.get_token_type(values['-SPLIT TYPE-'])
        gui.update_split_attrs(values, window)
    else:
        print('Unhandled event:', event)

    return listbox_notes, all_notes


if __name__ == '__main__':
    run_main_menu()

"""This module runs the entire application."""
import os
import re
import webbrowser
from tkinter import filedialog
from typing import Callable
from typing import Literal
from typing import Union

from note_splitter import gui
from note_splitter import note
from note_splitter import patterns
from note_splitter import tokens
from note_splitter.formatter_ import Formatter
from note_splitter.lexer import Lexer
from note_splitter.parser_ import AST
from note_splitter.settings import init_settings
from note_splitter.splitter import Splitter
from PySide6 import QtCore


def run_main_menu() -> None:
    """Displays the main menu."""
    init_settings()
    sg.theme("TanBlue")
    window = gui.create_main_menu_window()
    listbox_notes: list[note.Note] = []
    all_notes: list[note.Note] = []
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Close"):
            window.close()
            return
        listbox_notes, all_notes = handle_main_menu_event(
            event, values, window, listbox_notes, all_notes
        )


def split_files(window: sg.Window, notes: list[note.Note] = None) -> list[note.Note]:
    """Splits files into multiple smaller files.

    If no notes are provided, they will be found using the split keyword
    and the source folder path chosen in settings.

    Parameters
    ----------
    window : sg.Window
        The main menu window.
    notes : list[note.Note]
        The notes to be split.

    Returns
    -------
    new_notes : list[note.Note]
        The newly created notes.
    """
    tokenize: Callable = Lexer()
    split: Callable = Splitter()
    format_: Callable = Formatter()

    notes = notes or note.get_chosen_notes(window)
    all_new_notes: list[note.Note] = []
    settings = QtCore.QSettings()
    for i, source_note in enumerate(notes):
        gui.show_progress(i, len(notes), 1, 5)
        with open(source_note.path, "r", encoding="utf8") as file:
            content: str = file.read()
        gui.show_progress(i, len(notes), 2, 5)
        split_contents: list[str] = split_text(content, tokenize, split, format_)
        gui.show_progress(i, len(notes), 3, 5)
        new_file_names: list[str] = note.create_file_names(
            source_note.ext, split_contents
        )
        gui.show_progress(i, len(notes), 4, 5)
        new_notes = save_new_notes(split_contents, new_file_names, window)
        all_new_notes.extend(new_notes)
        gui.show_progress(i, len(notes), 5, 5)
        print(f"Created {len(new_notes)} new files.")
        if new_notes:
            if settings.value("create_index_file"):
                index_note: note.Note = create_index_file_(source_note, new_notes)
                print(f"Created index file at {index_note.path}")
                all_new_notes.append(index_note)
                if settings.value("create_backlinks"):
                    append_backlinks(index_note, new_notes)
            elif settings.value("create_backlinks"):
                append_backlinks(source_note, new_notes)

    return all_new_notes


def split_text(
    content: str, tokenize: Callable, split: Callable, format_: Callable
) -> list[str]:
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
    split_contents : list[str]
        A list of strings that are the sections of the original string.
    """
    tokens_: list[tokens.Token] = tokenize(content)
    ast = AST(tokens_, QtCore.QSettings().value("parse_blocks"))
    sections, global_tags = split(ast.content)
    split_contents: list[str] = format_(
        sections, global_tags, ast.frontmatter, ast.footnotes
    )
    return split_contents


def save_new_notes(
    split_contents: list[str], new_file_names: list[str], window: sg.Window
) -> list[note.Note]:
    """Creates new files and saves strings into them.

    The lists for the contents and names of the new files are parallel.

    Attributes
    ----------
    split_contents : list[str]
        A list of strings to each be saved into a new file.
    new_file_names : list[str]
        A list of names of files to be created.
    window : sg.Window
        The main menu window.

    Returns
    -------
    new_notes : list[note.Note]
        The newly created notes.
    """
    new_notes = []
    settings = QtCore.QSettings()
    for new_file_name, split_content in zip(new_file_names, split_contents):
        if not settings.value("destination_folder_path") or not os.path.exists(
            settings.value("destination_folder_path")
        ):
            settings.setValue(
                "destination_folder_path", note.require_folder_path("destination")
            )
            window["-DESTINATION FOLDER-"].update(
                settings.value("destination_folder_path")
            )
        new_file_path = os.path.join(
            settings.value("destination_folder_path"), new_file_name
        )
        new_file_path = note.ensure_file_path_uniqueness(new_file_path)
        if settings.value("destination_folder_path") != settings.value(
            "source_folder_path"
        ):
            split_content = note.make_file_paths_absolute(split_content, new_file_path)
        with open(new_file_path, "x", encoding="utf8") as file:
            file.write(split_content)
        new_notes.append(note.Note(new_file_path))
    return new_notes


def create_index_file_(source_note: note.Note, new_notes: list[note.Note]) -> note.Note:
    """Creates an index file for the new notes in the same folder.

    Parameters
    ----------
    source_note : note.Note
        The note that the new notes were created from.
    new_notes : list[note.Note]
        The newly created notes.

    Returns
    -------
    note.Note
        The newly created index Note.
    """
    index_name = note.validate_file_name(f"index - {source_note.title}.md", 35)
    folder_path = new_notes[0].folder_path
    index_file_path = os.path.join(folder_path, index_name)
    index_file_path = note.ensure_file_path_uniqueness(index_file_path)
    with open(index_file_path, "x", encoding="utf8") as file:
        file.write(f"# index of {source_note.title}\n\n")
        for n in new_notes:
            file.write(f"* [{n.title}]({n.path})\n")
        file.write(f"\n[Source: {source_note.title}]({source_note.path})")
    return note.Note(index_file_path, folder_path, index_name)


def append_backlinks(root_note: note.Note, notes: list[note.Note]) -> None:
    """Appends backlinks to the root note in each of the given notes.

    Parameters
    ----------
    root_note : str
        The note that the backlinks will link to.
    notes : list[note.Note]
        The notes to append backlinks to.
    """
    for note_ in notes:
        with open(note_.path, "a", encoding="utf8") as file:
            file.write(f"\n\n[Backlink: {root_note.title}]({root_note.path})\n")


def handle_main_menu_event(
    event: str,
    values: dict,
    window: sg.Window,
    listbox_notes: list[note.Note],
    all_notes: list[note.Note],
) -> tuple[list[note.Note], list[note.Note]]:
    """Handles the main menu's events.

    Parameters
    ----------
    event : str
        The event that occurred.
    values : dict
        The values of the widgets in the main menu.
    window : sg.Window
        The main menu window.
    listbox_notes : list[note.Note]
        The notes displayed in the listbox. This list may be empty.
    all_notes : list[note.Note]
        All of the user's notes. This list may be empty.

    Returns
    -------
    listbox_notes : list[note.Note]
        The notes displayed in the listbox. This list may be empty.
    all_notes : list[note.Note]
        All of the user's notes. This list may be empty.
    """
    settings = QtCore.QSettings()
    if event.startswith("URL "):
        url = event.split(" ")[1]
        webbrowser.open(url)
    elif event.startswith("change_") and event.endswith("_pattern"):
        setting_name = event[7:]
        settings.setValue(setting_name, values[event])
        patterns.__dict__[setting_name[:-8]] = re.compile(settings.value(setting_name))
    elif event == "open file browser":
        all_notes = note.get_all_notes(window)
        file_paths: Union[Literal[""], tuple[str, ...]] = filedialog.askopenfilenames()
        if not file_paths:
            return listbox_notes, all_notes
        listbox_notes = [note.Note(f) for f in file_paths]
        titles: list[str] = [n.title for n in listbox_notes]
        window["-NOTES TO SPLIT-"].update(values=titles)
        settings.setValue("using_split_keyword", False)
    elif event == "find by keyword":
        settings.setValue("using_split_keyword", True)
        all_notes = note.get_all_notes(window)
        listbox_notes = note.get_chosen_notes(window, all_notes)
        titles = [n.title for n in listbox_notes]
        window["-NOTES TO SPLIT-"].update(values=titles)
    elif event == "Split all":
        new_notes: list[note.Note] = split_files(window, listbox_notes)
        gui.run_split_summary_window(new_notes, all_notes)
        window["-NOTES TO SPLIT-"].update(values=[])
    elif event == "Split selected":
        notes_to_split = [
            note.get_by_title(listbox_notes, title)
            for title in values["-NOTES TO SPLIT-"]
        ]
        if not notes_to_split:
            sg.popup("No notes selected.", keep_on_top=True)
        else:
            new_notes = split_files(window, notes_to_split)
            gui.run_split_summary_window(new_notes, all_notes)
            listbox_notes = [
                n for n in listbox_notes if n.title not in values["-NOTES TO SPLIT-"]
            ]
            titles = [n.title for n in listbox_notes]
            window["-NOTES TO SPLIT-"].update(values=titles)
    elif event == "parseBlocks":
        settings.setValue("parse_blocks", values["parseBlocks"])
        gui.update_split_type_and_attrs(values, window)
    elif event == "-SPLIT TYPE-":
        settings.setValue("split_type", values["-SPLIT TYPE-"])
        gui.update_split_attrs(values, window)
    elif event in ("-SPLIT ATTR-", "-SPLIT ATTR VALUE-"):
        settings.setValue(
            "split_attrs", {values["-SPLIT ATTR-"]: values["-SPLIT ATTR VALUE-"]}
        )
    elif event == "-SPLIT KEYWORD-":
        settings.setValue("split_keyword", values["-SPLIT KEYWORD-"])
    elif event == "-SOURCE FOLDER-":
        settings.setValue("source_folder_path", values["-SOURCE FOLDER-"])
    elif event == "-DESTINATION FOLDER-":
        settings.setValue("destination_folder_path", values["-DESTINATION FOLDER-"])
    elif event == "-FILE NAME FORMAT-":
        settings.setValue("file_name_format", values["-FILE NAME FORMAT-"])
    elif event == "indexFile":
        settings.setValue("create_index_file", values["indexFile"])
    elif event == "remove_split_keyword":
        settings.setValue("remove_split_keyword", values["remove_split_keyword"])
    elif event == "move_footnotes":
        settings.setValue("move_footnotes", values["move_footnotes"])
    elif event == "copy_frontmatter":
        settings.setValue("copy_frontmatter", values["copy_frontmatter"])
    elif event == "copy_global_tags":
        settings.setValue("copy_global_tags", values["copy_global_tags"])
    elif event == "create_backlinks":
        settings.setValue("create_backlinks", values["create_backlinks"])
    else:
        print("Unhandled event:", event)

    return listbox_notes, all_notes


if __name__ == "__main__":
    run_main_menu()

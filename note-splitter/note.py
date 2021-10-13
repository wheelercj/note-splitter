# external imports
import os
from typing import List

# internal imports
import settings


class Note:
    """Info about one of the user's note files.
    
    Attributes
    ----------
    path: str
        The absolute path to the file.
    folder_path : str
        The absolute path to the folder that the file is in.
    name : str
        The name of the file, including the file extension.
    """
    def __init__(self, path: str, folder_path: str, name: str):
        self.path = path
        self.folder_path = folder_path
        self.name = name


def get_chosen_notes() -> List[Note]:
    """Gets the notes that the user chose to split."""
    chosen_notes: List[Note] = []
    all_notes: List[Note] = get_all_notes()
    for note in all_notes:
        with open(note.path, 'r', encoding='utf8') as file:
            contents = file.read()
        if settings.split_keyword in contents:
            chosen_notes.append(note)
    return chosen_notes


def get_all_notes() -> List[Note]:
    """Gets all the notes in the user's chosen folder."""
    notes: List[Note] = []
    folder_path = settings.source_folder_path
    folder_list = os.listdir(folder_path)
    for file_name in folder_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file_name)
            if file_ext in settings.note_types:
                notes.append(Note(file_path, folder_path, file_name))

    return notes

# external imports
import os
from typing import List
from datetime import datetime, timedelta

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


def create_time_id_file_names(file_ext: str, file_count: int = 1) -> List[str]:
    """Creates file names with increasing 14-digit numbers.
    
    The file extension must start with a period. The numbers in the 
    returned file names represent the time in the format YYYYMMDDhhmmss,
    starting with the current time and increasing by one second for each
    file created.
    """
    file_names = []
    now = datetime.now()
    file_names.append(create_time_id_file_name(now, file_ext))
    for _ in range(file_count):
        now += timedelta(seconds=1)
        file_names.append(create_time_id_file_name(now, file_ext))
    return file_names


def create_time_id_file_name(dt: datetime, file_ext: str) -> str:
    """Creates a file name with the given datetime."""
    year = str(dt.year)
    month = str(dt.month).zfill(2)
    day = str(dt.day).zfill(2)
    hour = str(dt.hour).zfill(2)
    minute = str(dt.minute).zfill(2)
    second = str(dt.second).zfill(2)
    return f'{year}{month}{day}{hour}{minute}{second}{file_ext}'

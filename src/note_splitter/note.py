"""Manages info about the user's files."""


import os
from typing import List, Optional
from datetime import datetime, timedelta
from note_splitter import settings


class Note:
    """Info about one of the user's note files.
    
    Attributes
    ----------
    title : str
        The title of the note. This is the body of the first header, or 
        the first line of the file if there is no header.
    name : str
        The name of the file, including the file extension.
    ext : str
        The file extension, starting with a period.
    path : str
        The absolute path to the file.
    folder_path : str
        The absolute path to the folder that the file is in.
    """
    def __init__(self, path: str, folder_path: str = None, name: str = None):
        """Creates a new Note object.

        Parameters
        ----------
        path : str
            The absolute path to the file.
        folder_path : str
            The absolute path to the folder that the file is in. If not
            provided, it will be retrieved from the path.
        name : str
            The name of the file, including the file extension. If not
            provided, it will be retrieved from the path.
        """
        self.path = path
        if folder_path is None:
            self.folder_path = os.path.dirname(path)
        else:
            self.folder_path = folder_path
        if name is None:
            self.name = os.path.basename(path)
        else:
            self.name = name
        self.ext = os.path.splitext(self.path)[1]
        self.title = self.get_title()


    def get_title(self) -> str:
        """Returns the title of the note."""
        with open(self.path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    return line.lstrip('#').strip()
            return file.readline().strip()


def get_chosen_notes(all_notes: Optional[List[Note]] = None) -> List[Note]:
    """Gets the notes that the user chose to split.
    
    Parameters
    ----------
    all_notes : List[Note], optional
        The list of all the notes in the user's chosen folder. If not 
        provided, the list of all the notes in the user's chosen folder 
        will be retrieved.
    """
    if all_notes is None:
        all_notes: List[Note] = get_all_notes()

    chosen_notes: List[Note] = []
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
    if not folder_path:
        pass  # TODO: prompt the user for a valid folder path instead.
    try:
        folder_list = os.listdir(folder_path)
    except FileNotFoundError:
        print(f'Folder {folder_path} does not exist.')
        raise  # TODO: prompt the user for a valid folder path instead.
    
    for file_name in folder_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            _, file_ext = os.path.splitext(file_name)
            if file_ext in settings.note_types:
                notes.append(Note(file_path, folder_path, file_name))

    return notes


def create_time_id_file_names(file_ext: str, file_count: int = 1) -> List[str]:
    """Creates file names with increasing 14-digit numbers.
    
    The file extension must start with a period. The numbers in the 
    returned file names represent the time in the format YYYYMMDDhhmmss,
    starting with the current time and increasing by one second for each
    file created.

    Parameters
    ----------
    file_ext : str
        The file extension, including the period.
    file_count : int, optional
        The number of files to create. The default is 1.
    """
    file_names = []
    now = datetime.now()
    file_names.append(__create_time_id_file_name(now, file_ext))
    for _ in range(file_count):
        now += timedelta(seconds=1)
        file_names.append(__create_time_id_file_name(now, file_ext))
    return file_names


def __create_time_id_file_name(dt: datetime, file_ext: str) -> str:
    """Creates a file name with the given datetime.
    
    The part of the file name before the extension will be in the format
    YYYYMMDDhhmmss.

    Parameters
    ----------
    dt : datetime
        The datetime to use in the file name.
    file_ext : str
        The file extension, including the period.
    """
    year = str(dt.year)
    month = str(dt.month).zfill(2)
    day = str(dt.day).zfill(2)
    hour = str(dt.hour).zfill(2)
    minute = str(dt.minute).zfill(2)
    second = str(dt.second).zfill(2)
    return f'{year}{month}{day}{hour}{minute}{second}{file_ext}'

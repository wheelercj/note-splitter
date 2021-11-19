"""Manages info about the user's files."""


import os
import uuid
from copy import copy
from typing import List, Tuple
from datetime import datetime, timedelta
from note_splitter import settings
from note_splitter.patterns import any_header as header_pattern


class Note:
    """Info about one of the user's note files.
    
    Attributes
    ----------
    title : str
        The title of the note. This is the body of the first header, or 
        the first line of the file if there is no header, or an empty 
        string if the file is empty.
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

        Assumes that the file already exists and has its content.

        Parameters
        ----------
        path : str
            The absolute path to the file.
        folder_path : str, optional
            The absolute path to the folder that the file is in. If not
            provided, it will be retrieved from the path.
        name : str, optional
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
        with open(self.path, 'r', encoding='utf8') as file:
            contents = file.read()
        self.title = get_title(contents)


def get_chosen_notes(all_notes: List[Note] = None) -> List[Note]:
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


def create_file_names(file_ext: str, files_contents: List[str]) -> List[str]:
    """Creates names for new files.

    The returned file names are in the format specified in the
    file_name_format setting. If more than one file name is created and 
    file_name_format contains an at least one hour, minute, or seconds 
    variable, the time will be incremented for each file name.

    Parameters
    ----------
    file_ext : str
        The file extension, including the leading period.
    files_contents : List[str]
        The contents of the files to be named.
    """
    file_names = []
    now = datetime.now()
    for file_contents in files_contents:
        file_name_format = copy(settings.file_name_format)
        new_file_name = __create_file_name(file_ext,
                                           file_name_format,
                                           file_contents,
                                           now)
        new_file_name = validate_file_name(new_file_name)
        file_names.append(new_file_name)
        if r'%s' in file_name_format:
            now += timedelta(seconds=1)
        elif r'%m' in file_name_format:
            now += timedelta(minutes=1)
        elif r'%h' in file_name_format:
            now += timedelta(hours=1)
        elif r'%D' in file_name_format:
            now += timedelta(days=1)            
    return file_names


def __create_file_name(file_ext: str,
                       file_name_format: str,
                       file_contents: str,
                       dt: datetime) -> str:
    """Creates a name for a new file.

    Parameters
    ----------
    file_ext : str
        The file extension, including the leading period.
    file_name_format : str
        The format of the file name.
    file_contents : str
        The contents of the file to be named.
    dt : datetime
        The date and time to use for the file name if the file name
        format contains any date and/or time variables.
    """
    if not file_name_format:
        file_name_format = r'%uuid4'
    variables = __get_variables(file_contents, dt)
    variables.append((r'%id', create_file_id(file_contents, dt)))
    for name, value in variables:
        file_name_format = file_name_format.replace(name, value)
    return f'{file_name_format}{file_ext}'


def create_file_id(file_contents: str, dt: datetime = None) -> str:
    """Creates an ID for a file.
    
    This function depends on the file_id_format setting.

    Parameters
    ----------
    file_contents : str
        The contents of the file to be IDed.
    dt : datetime, optional
        The datetime to use in the file name. If not provided, the 
        current time will be used.
    """
    if dt is None:
        dt = datetime.now()
    file_id = copy(settings.file_id_format)
    variables = __get_variables(file_contents, dt)
    for name, value in variables:
        file_id = file_id.replace(name, value)
    return file_id


def __get_variables(file_contents: str, dt: datetime) -> List[Tuple[str, str]]:
    """Gets the variable names and values for file name and ID formats.

    Parameters
    ----------
    file_contents : str
        The contents of the file being named or IDed.
    dt : datetime
        The datetime to use in the file name or ID if the format
        contains any date and/or time variables.
    """
    return [
        (r'%uuid4', str(uuid.uuid4())),
        (r'%title', get_title(file_contents)),
        (r'%Y', str(dt.year)),
        (r'%M', str(dt.month).zfill(2)),
        (r'%D', str(dt.day).zfill(2)),
        (r'%h', str(dt.hour).zfill(2)),
        (r'%m', str(dt.minute).zfill(2)),
        (r'%s', str(dt.second).zfill(2)),
    ]


def get_title(file_contents: str) -> str:
    """Gets the title of the file.
    
    The title is the body of the first header, or the first line if 
    there is no header, or a random string if the file is empty.

    Parameters
    ----------
    file_contents : str
        The contents of the file to get the title from.
    """
    for line in file_contents.split('\n'):
        if header_pattern.match(line):
            return line.lstrip('#').strip()
    title = file_contents.split('\n')[0].strip()
    if title:
        return title
    return str(uuid.uuid4())


def validate_file_name(file_name: str, max_length: int = 30) -> str:
    """Validates a file name's characters and length.

    Invalid characters are replaced with hyphens. If the file name has a
    length greater than max_length, it is truncated. If the file name 
    starts or ends with certain characters, they are removed.

    Parameters
    ----------
    file_name : str
        The file name to validate.
    max_length : int, optional
        The maximum length of the file name.

    Returns
    -------
    file_name : str
        The validated file name.
    """
    root, ext = os.path.splitext(file_name)
    root = root[:max_length]
    invalid_characters = '#%{&}\\<>*?/$!\'":@+`|='
    for ch in invalid_characters:
        root = root.replace(ch, '-')
    invalid_start_or_end_characters = ' .-_'
    for ch in invalid_start_or_end_characters:
        root = root.lstrip(ch).rstrip(ch)
    print(f'{root}{ext}')
    return root + ext

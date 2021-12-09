"""PySimpleGUI Note Splitter Demo Program Project GUI

    PySimpleGUI was used to create a note splitter that can be used as a general purpose tool. 

    The basic file operations are
      * Upload a file
      * Split a file
      * Filter by desired settings
      * Search in files
      * Run a regular expression search on all files
      * Display example of split of file(s) in a GUI tab
    
    Additional operations
      * Edit this file type in editor

    ## settings on the Home tab
      * split type
      * split attributes
      * source folder path
      * create blocks

    ## settings on the Settings tab
      * split keyword
      * new file name format
      * create index file
      * copy frontmatter
      * copy global tags
      * backlink

    ## settings to keep hidden for now
      * destination folder path
      * note types
      * replace split contents
     
    Keeps a "history" of the previously chosen settings to easy switching between projects
                
    Copyright 2021 Note Splitter
"""

import PySimpleGUI as sg  # https://pysimplegui.readthedocs.io/en/latest/
from typing import Tuple, List, Optional
from note_splitter import settings, note


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


def create_main_menu_window() -> sg.Window:
    """Creates the main menu window."""
    window = sg.Window('Note Splitter',
                       create_main_menu_layout(),
                       grab_anywhere=True,
                       resizable=True,
                       margins=(0,0),
                       use_custom_titlebar=True,
                       finalize=True)
    window.set_min_size(window.size)
    return window


def create_main_menu_layout() -> List[List[sg.Element]]:
    """Creates the main menu's layout."""
    menu_def = [
        ['&Close Application', ['C&lose']],
        ['&Help', ['&Tips']]]
    tabgroup_layout = [
        [sg.Tab('Home', create_home_tab_layout()),
         sg.Tab('Settings', create_settings_tab_layout()),
         sg.Tab('About', create_about_tab_layout())]]
    layout = [
        [sg.MenubarCustom(menu_def,
                          key='-MENU-',
                          font='Courier 15',
                          tearoff=True)],
        [sg.Text('Note Splitter',
                 size=(38, 1),
                 justification='center',
                 font=("Helvetica", 16),
                 relief=sg.RELIEF_RIDGE,
                 k='-TEXT HEADING-',
                 enable_events=True)],
        [sg.TabGroup(tabgroup_layout,
                     key='-TAB GROUP-',
                     expand_x=True,
                     expand_y=True)]]
    layout[-1].append(sg.Sizegrip())
    return layout


def create_home_tab_layout() -> List[List[sg.Element]]:
    """Creates the home tab's layout."""
    frame_layout = [
        [sg.T('Choose which files to split: ')],
        [sg.Button('Open File'),
         sg.T(' or '),
         sg.Button('find'),
         sg.T(' by ')],
        [sg.Text('keyword:'),
         sg.InputText(settings.split_keyword)]]
    tab_layout = [
        [sg.Frame('',
                  frame_layout,
                  font='Any 12',
                  title_color='blue')],
        [sg.T('Files to split:')]]
    tab_layout.extend(create_note_listbox_layout(None, '-NOTES TO SPLIT-'))
    tab_layout.extend([
        [sg.Text('Choose what to split by: ')],
        [sg.Text('type                                            attribute         value')],
        [create_split_type_dropdown(),
         create_split_attr_dropdown(),
         sg.InputText(settings.split_attrs.get('level', ''))],
        [sg.Checkbox('parse blocks',
                     key='createBlocks',
                     default=settings.parse_blocks)],
        [sg.Button('Split all'),
         sg.Button('Split selected'),
         sg.Button('Close')]])

    return tab_layout


def create_settings_tab_layout() -> List[List[sg.Element]]:
    """Creates the settings tab's layout."""
    return [
        [sg.Text('Source Folder',
                 size=(15, 1),
                 auto_size_text=False,
                 justification='right'),
         sg.InputText(settings.source_folder_path),
         sg.FolderBrowse()],
        [sg.Text('Destination Folder',
                 size=(15, 1),
                 auto_size_text=False,
                 justification='right'),
         sg.InputText(settings.destination_folder_path),
         sg.FolderBrowse()],
        [sg.Text("New file name format"),
         sg.Input(settings.file_name_format)],
        [sg.Checkbox('create index file',
                     key='indexFile',
                     default=settings.create_index_file)],
        [sg.Checkbox('copy frontmatter',
                     key='copy_frontmatter',
                     default=settings.copy_frontmatter)],
        [sg.Checkbox('copy global tags',
                     key='copy_global_tags',
                     default=settings.copy_global_tags)],
        [sg.Checkbox('backlink',
                     key='backlink',
                     default=settings.backlink)]]
        # [sg.Text("Change the theme of Note Splitter to your liking.")],
        # [sg.Listbox(values = sg.theme_list(), 
        #             size =(20, 12), 
        #             key ='-THEME LISTBOX-',
        #             enable_events = True)],
        # [sg.Button("Set Theme")],


def create_about_tab_layout() -> List[List[sg.Element]]:
    """Creates the about tab's layout."""
    return [
        [sg.Text('•', font=('Arial', 16)),
         create_hyperlink('instructions',
                          'https://github.com/wheelercj/note-splitter/blob/master/README.md')],
        [sg.Text('•', font=('Arial', 16)),
         create_hyperlink('request a feature or report a bug',
                          'https://github.com/wheelercj/note-splitter/issues')],
        [sg.Text('•', font=('Arial', 16)),
         create_hyperlink('join the discussion',
                          'https://github.com/wheelercj/note-splitter/discussions')],
        [sg.Text('•', font=('Arial', 16)),
         create_hyperlink('browse the developer documentation',
                          'https://note-splitter.readthedocs.io/en/latest/')],
        [sg.Text('•', font=('Arial', 16)),
         create_hyperlink('see the software license',
                          'https://github.com/wheelercj/note-splitter/blob/master/LICENSE')]]


def create_hyperlink(text: str,
                     url: str,
                     font: Tuple[str, int, str] = None) -> sg.Text:
    """Creates a PySimpleGUI Text object with a clickable hyperlink.

    When the user clicks the hyperlink, the event created will start 
    with 'URL ' and end with the URL.
    
    Parameters
    ----------
    text : str
        The text to display in the Text object.
    url : str
        The URL to open when the hyperlink is clicked.
    font : Tuple[str, int, str]
        The font to use for the Text object. The first element is the 
        font family, the second is the font size, and the third is the
        font style. The default is ('Arial', 14, 'underline').

    Returns
    -------
    sg.Text
        A PySimpleGUI Text object with a clickable hyperlink.
    """
    if font is None:
        font = ('Arial', 14, 'underline')
    return sg.Text(text,
                   tooltip=url,
                   enable_events=True,
                   font=font,
                   key=f'URL {url}')


def create_split_type_dropdown() -> sg.Combo:
    """Creates a dropdown element listing token types.
    
    The Section type is excluded.
    """
    token_type_names = settings.get_all_token_type_names()
    token_type_names.remove('section')
    default_split_type_name = settings.get_token_type_name(settings.split_type)
    return sg.Combo(values=token_type_names,
                    default_value=default_split_type_name,
                    key='-SPLIT TYPE-')


def create_split_attr_dropdown() -> sg.Combo:
    """Creates a dropdown element listing token attributes and None."""
    obj = settings.split_type()
    attr_names: List[str] = list(obj.__dict__.keys())
    attr_names.append(None)
    return sg.Combo(values=attr_names,
                    default_value='level' if 'level' in attr_names else None,
                    key='-SPLIT ATTR-')


def create_split_summary_window(notes: List[note.Note],
                                listbox_key: str) -> sg.Window:
    """Creates a window displaying the number of notes split.
    
    Parameters
    ----------
    notes : List[note.Note]
        The notes displayed in the listbox.
    listbox_key : str
        The key of the listbox.
    """
    splitsummary_layout = [
        [sg.T(f'Number of new files created: {len(notes)}')]]
    listbox_layout = create_note_listbox_layout_with_buttons(notes,
                                                             listbox_key)
    splitsummary_layout.extend(listbox_layout)
    splitsummary_layout.extend([
        [sg.HorizontalSeparator()],
        [sg.Button('OK', key='OK')]])
    return sg.Window('Split Summary', splitsummary_layout)


def run_split_summary_window(notes: List[note.Note],
                             all_notes: List[note.Note]) -> None:
    """Runs the split summary window.
    
    Parameters
    ----------
    notes : List[note.Note]
        The notes displayed in the listbox.
    """
    listbox_key = '-LISTBOX-'
    window = create_split_summary_window(notes, listbox_key)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            window.close()
            return
        handle_note_listbox_event(event,
                                  values,
                                  window,
                                  notes,
                                  listbox_key,
                                  all_notes)


def create_note_listbox_layout_with_buttons(
        notes: List[note.Note],
        key: str) -> List[List[sg.Element]]:
    """Creates a listbox of note titles and relevant buttons.

    The listbox itself has the given key, and the buttons have these 
    keys: ``f'-OPEN{key}'`` for the "Open" button, ``f'-DELETE{key}'`` 
    for the "Delete" button, ``f'-MOVE{key}'`` for the "Move" button, 
    and ``f'-SHOW{key}'`` for the "Show in file browser" button.
    
    Parameters
    ----------
    notes : List[note.Note]
        The notes to display in the listbox.
    key : str
        The key to use for the listbox and part of each of its buttons.
    """
    layout = create_note_listbox_layout(notes, key)
    layout.append([
        sg.Button('Open', key=f'-OPEN{key}'),
        sg.Button('Delete', key=f'-DELETE{key}'),
        sg.Button('Move', key=f'-MOVE{key}'),
        sg.Button('Show in file browser', key=f'-SHOW{key}')
    ])
    return layout


def create_note_listbox_layout(notes: Optional[List[note.Note]],
                               key: str) -> List[List[sg.Element]]:
    """Creates a listbox of note titles.

    Parameters
    ----------
    notes : List[note.Note], optional
        The notes to display in the listbox.
    key : str
        The key to use for the listbox.
    """
    if notes is None:
        note_titles = []
    else:
        note_titles = [n.title for n in notes]
    return [[sg.Listbox(note_titles, key=key, size=(80, 6))]]


def handle_note_listbox_event(event: str,
                              values,
                              window,
                              listbox_notes: List[note.Note],
                              listbox_key: str,
                              all_notes: List[note.Note]) -> None:
    """Handles an event from a listbox of notes.

    Parameters
    ----------
    event : str
        The event to handle.
    values : Any
        The value of the event.
    window : sg.Window
        The window containing the listbox.
    listbox_notes : List[note.Note]
        The notes displayed in the listbox.
    listbox_key : str
        The key of the listbox.
    all_notes : List[note.Note]
        All of the user's notes.
    """
    listbox_notes_dict = {n.title: n for n in listbox_notes}
    selected_titles = values[listbox_key]
    if not selected_titles:
        selected_titles = [str(key) for key in listbox_notes_dict.keys()]
    if event.startswith('-DELETE'):
        answer = sg.popup_yes_no('Are you sure you want to delete notes?',
                                 keep_on_top=True)
        if answer != 'Yes':
            return
    for title in selected_titles:
            note_: note.Note = listbox_notes_dict[title]
            if event.startswith('-OPEN'):
                if note_.open() is None:
                    del listbox_notes_dict[note_.title]
            if event.startswith('-SHOW'):
                if note_.show() is None:
                    del listbox_notes_dict[note_.title]
            if event.startswith('-MOVE'):
                dest_path = note.request_folder_path('destination')
                if dest_path:
                    if note_.move(dest_path, all_notes) is None:
                        del listbox_notes_dict[note_.title]
            if event.startswith('-DELETE'):
                note_.delete()
                del listbox_notes_dict[note_.title]
    window[listbox_key].update(values=listbox_notes_dict.keys())

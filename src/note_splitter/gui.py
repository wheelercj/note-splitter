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
import webbrowser
from typing import Tuple, List, Optional
from note_splitter import settings
from note_splitter.note import Note


def make_window(theme) -> sg.Window:
    sg.theme(theme)
    menu_def = [['&Close Application', ['Q&uit']],
                ['&Help', ['&Tips']] ]

    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
                [sg.Text('Note Splitter', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    layout +=[[sg.TabGroup([[  sg.Tab('Home', create_home_tab_layout()),
                               sg.Tab('Settings', create_settings_layout()),
                               sg.Tab('Documentation', create_help_layout())]],
                            key='-TAB GROUP-', expand_x=True, expand_y=True)]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Note Splitter Demo and GUI', layout, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window.set_min_size(window.size)
    return window


def main():
    window = make_window(sg.theme())
    
    # This is an event Loop 
    while True:
        event, values = window.read(timeout=100)

        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
        if event in (None, 'Quit'):
            break
        elif event == 'Tips':
            sg.popup('Visit each of the tabs to see available applications.',
                     'Various tabs are included such as development environment setup, Note Splitter overview, token hierarchy, program modules, references, and how the documentation is maintained.',
                     'If you have any questions or concerns please message the developers on the GitHub page.', keep_on_top=True)
        elif event.startswith('URL '):
            url = event.split(' ')[1]
            webbrowser.open(url)
        elif event == 'Split Summary':
            run_split_summary_window(new_notes)
        elif event == "Open Folder":
            folder_or_file = sg.popup_get_folder('Choose your folder', keep_on_top=True)
            sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
        elif event == "Open File":
            folder_or_file = sg.popup_get_file('Choose your file', keep_on_top=True)
            sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
        elif event == "Set Theme":
            theme_chosen = values['-THEME LISTBOX-'][0]
            window.close()
            window = make_window(theme_chosen)
        elif event == 'Versions':
            sg.popup(sg.get_versions(), keep_on_top=True)

    window.close()
    exit(0)


def create_home_tab_layout() -> List[List[sg.Element]]:
    """Creates the home tab's layout."""
    frame_layout = [[sg.T('Choose which files to split: ')],
                [sg.Button("Open File"), sg.T(' or '), sg.Button("find"), sg.T(' by ')],
                [sg.Text('keyword:', size =(15, 1)), sg.InputText()]]
    
    input_layout =  [[sg.Frame('', frame_layout, font='Any 12', title_color='blue')],
                     [sg.T('Files to split:')]]
    input_layout.extend(create_note_listbox_layout(None, '-NOTES TO SPLIT-'))  # TODO: use something instead of None.
    input_layout.extend([
                [sg.Text('Choose what to split by: ')],
                [sg.Text('type                attribute           value')],
                [create_split_type_dropdown(),
                 create_split_attr_dropdown(),
                 sg.Text('Enter a number: ', size=(15, 1)), sg.InputText()],
                [sg.Checkbox('create blocks', key='createBlocks')],
                
                [sg.Button('Split all'), sg.Button('Split selected'), sg.Button('Quit')]])

    return input_layout


def create_settings_layout() -> List[List[sg.Element]]:
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
        [sg.Text("New file name format"), sg.Input(settings.file_name_format)],
        [sg.Checkbox('create index file',key='indexFile')],
        [sg.Checkbox('copy frontmatter',key='copy_frontmatter')],
        [sg.Checkbox('copy global tags',key='copy_global_tags')],
        [sg.Checkbox('backlink',key='backlink')],
        # [sg.Text("Change the theme of Note Splitter to your liking.")],
        #             [sg.Listbox(values = sg.theme_list(), 
        #               size =(20, 12), 
        #               key ='-THEME LISTBOX-',
        #               enable_events = True)],
        #               [sg.Button("Set Theme")],
        [sg.Button('Save')]]


def create_help_layout() -> List[List[sg.Element]]:
    """Creates the help tab's layout."""
    return [[create_hyperlink('Click here for the documentation', 'https://note-splitter.readthedocs.io/en/latest/') ]]


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
        font style. The default is ('Arial', 18, 'underline').

    Returns
    -------
    sg.Text
        A PySimpleGUI Text object with a clickable hyperlink.
    """
    if font is None:
        font = ('Arial', 18, 'underline')
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
    return sg.Combo(values=token_type_names,
                    default_value='header',
                    key='-SPLIT TYPE-')


def create_split_attr_dropdown() -> sg.Combo:
    """Creates a dropdown element listing token attributes."""
    obj = settings.split_type()
    attr_names: List[str] = list(obj.__dict__.keys())
    default_value = 'level' if 'level' in attr_names else None
    return sg.Combo(values=attr_names,
                    default_value=default_value,
                    key='-SPLIT ATTR-')


def create_split_summary_window(notes: List[Note], listbox_key: str) -> sg.Window:
    """Creates a window displaying the number of notes split.
    
    Parameters
    ----------
    notes : List[Note]
        The notes displayed in the listbox.
    listbox_key : str
        The key of the listbox.
    """
    splitsummary_layout = [[sg.T(f'Number of new files created: {len(notes)}')]]
    listbox_layout = create_note_listbox_layout_with_buttons(notes, listbox_key)
    splitsummary_layout.extend(listbox_layout)
    splitsummary_layout.append([sg.Button('OK', key='OK')])
    return sg.Window('Split Summary', splitsummary_layout)


def run_split_summary_window(notes: List[Note]) -> None:
    """Runs the split summary window.
    
    Parameters
    ----------
    notes : List[Note]
        The notes displayed in the listbox.
    """
    listbox_key = '-LISTBOX-'
    window = create_split_summary_window(notes, listbox_key)
    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, 'OK'):
            window.close()
            return
        handle_note_listbox_event(event, values, notes, listbox_key)


def create_note_listbox_layout_with_buttons(
        notes: List[Note],
        key: str) -> List[List[sg.Element]]:
    """Creates a listbox of note titles and relevant buttons.

    The listbox itself has the given key, and the buttons have these 
    keys: 
     * ``f'-OPEN{key}'`` for the "Open" button
     * ``f'-DELETE{key}'`` for the "Delete" button
     * ``f'-MOVE{key}'`` for the "Move" button
     * ``f'-SHOW{key}'`` for the "Show in file browser" button
    
    Parameters
    ----------
    notes : List[Note]
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


def create_note_listbox_layout(notes: Optional[List[Note]],
                               key: str) -> List[List[sg.Element]]:
    """Creates a listbox of note titles.

    Parameters
    ----------
    notes : List[Note], optional
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
                              listbox_notes: List[Note],
                              listbox_key: str) -> None:
    """Handles an event from a listbox of notes.

    Parameters
    ----------
    event : str
        The event to handle.
    values : Any
        The value of the event.
    listbox_notes : List[Note]
        The notes displayed in the listbox.
    listbox_key : str
        The key of the listbox.
    """
    listbox_notes_dict = {n.title: n for n in listbox_notes}
    selected_titles = values[listbox_key]
    if event.startswith('-DELETE'):
        answer = sg.popup_yes_no('Are you sure you want to delete ' \
                            'the selected notes?', keep_on_top=True)
        if answer != 'Yes':
            return
    for title in selected_titles:
            note_: Note = listbox_notes_dict[title]
            if event.startswith('-OPEN'):
                if note_.open() is None:
                    listbox_notes.remove(note_)
            if event.startswith('-SHOW'):
                if note_.show() is None:
                    listbox_notes.remove(note_)
            if event.startswith('-MOVE'):
                if note_.move() is None:
                    listbox_notes.remove(note_)
            if event.startswith('-DELETE'):
                note_.delete()
                listbox_notes.remove(note_)


if __name__ == '__main__':
    sg.theme('TanBlue')
    main()

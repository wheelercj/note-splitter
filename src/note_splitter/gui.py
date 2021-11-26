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
from typing import Tuple, List, Dict
from note_splitter import settings
from note_splitter.note import Note


def make_window(theme):
    sg.theme(theme)
    menu_def = [['&Close Application', ['E&xit']],
                ['&Help', ['&Documentation']] ]
    right_click_menu_def = [[], ['Versions', 'Exit']]

    frame_layout = [[sg.T('Split by:')],
                  [sg.CB('Check 1'), sg.CB('Check 2'), sg.CB('Check 3')]]

    input_layout =  [
                [sg.Multiline('Note Splitter User Tips:\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nYou get the point.', size=(45,5), expand_x=True, expand_y=True, k='-MLINE-')],

                # [sg.Text("Choose some File"), sg.Input(key="-IN2-",change_submits=True), sg.FilesBrowse(key="-IN-")],

                [sg.Button("Open Folder")],
                [sg.Button("Open File")],

                [sg.Frame('', frame_layout, font='Any 12', title_color='blue')],

                [sg.Combo(values=('Combo 1', 'Combo 2', 'Combo 3'), default_value='Combo 1', readonly=True, k='-COMBO-'),

                 sg.OptionMenu(values=('Option 1', 'Option 2', 'Option 3'),  k='-OPTION MENU-'),],

                [sg.Button('Split'), sg.Button('Split Summary')]]

    logging_layout = [[sg.Text("Anything printed will display here!")],
                      [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                      # [sg.Output(size=(60,15), font='Courier 8', expand_x=True, expand_y=True)]
                      ]

    # specialty_layout = [[sg.Text("Any \"special\" elements will display here!")],
    #                   [sg.Button("Open Folder")],
    #                   [sg.Button("Open File")]]

    settings_layout = [[sg.Text("Any \"setting\" options will be chosen and displayed here!")]]
    
    theme_layout = [[sg.Text("Change the theme of Note Splitter to your liking.")],
                    [sg.Listbox(values = sg.theme_list(), 
                      size =(20, 12), 
                      key ='-THEME LISTBOX-',
                      enable_events = True)],
                      [sg.Button("Set Theme")]]
    
    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
                [sg.Text('Note Splitter', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    layout +=[[sg.TabGroup([[  sg.Tab('Home', input_layout),
                              #  sg.Tab('Dummy Tab', specialty_layout),
                               sg.Tab('Settings', settings_layout),                 sg.Tab('Change Theme', theme_layout),
                               sg.Tab('Output', logging_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

               ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Note Splitter Demo and GUI', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
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
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
        elif event == 'Documentation':
            print("[LOG] Clicked Documentation!")
            sg.popup('The following link is for the Note Splitter documentation:',
                     'note-splitter.readthedocs.io',
                     'Visit each of the tabs to see available applications.',
                     'Various tabs are included such as development environment setup, Note Splitter overview, token hierarchy, program modules, references, and how the documentation is maintained.',
                     'If you have any questions or concerns please message the developers on the GitHub page.', keep_on_top=True)
        elif event == 'Split Summary':
            print("[LOG] Clicked Popup Button!")
            sg.popup("The number of files split: ", keep_on_top=True)
            print("[LOG] Dismissing Popup!")
        elif event == "Open Folder":
            print("[LOG] Clicked Open Folder!")
            folder_or_file = sg.popup_get_folder('Choose your folder', keep_on_top=True)
            sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
            print("[LOG] User chose folder: " + str(folder_or_file))
        elif event == "Open File":
            print("[LOG] Clicked Open File!")
            folder_or_file = sg.popup_get_file('Choose your file', keep_on_top=True)
            sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
            print("[LOG] User chose file: " + str(folder_or_file))
        elif event == "Set Theme":
            print("[LOG] Clicked Set Theme!")
            theme_chosen = values['-THEME LISTBOX-'][0]
            print("[LOG] User Chose Theme: " + str(theme_chosen))
            window.close()
            window = make_window(theme_chosen)
        elif event == 'Versions':
            sg.popup(sg.get_versions(), keep_on_top=True)

    window.close()
    exit(0)


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


def create_note_listbox_layout(notes: List[Note],
                               key: str) -> List[List[sg.Element]]:
    """Creates a listbox of note titles and relevant buttons.

    The open and show buttons will have the keys ``f'-OPEN{key}'`` and
    ``f'-SHOW{key}'``, respectively.
    
    Parameters
    ----------
    notes : List[Note]
        The notes to display in the listbox.
    key : str
        The key to use for the listbox and part of each of its buttons.
    """
    note_titles = [n.title for n in notes]
    return [[sg.Listbox(note_titles, key=key, size=(80, 6))],
            [sg.Button('Open', key=f'-OPEN{key}'),
             sg.Button('Show in file browser', key=f'-SHOW{key}')]]


def handle_note_listbox_event(event: str,
                              selected_titles: List[str],
                              listbox_notes: List[Note]) -> None:
    """Handles an event from a listbox of notes.

    Parameters
    ----------
    event : str
        The event to handle.
    selected_titles : List[str]
        The titles of the notes selected in the listbox.
    listbox_notes : List[Note]
        The notes displayed in the listbox.
    """
    listbox_notes_dict = {n.title: n for n in listbox_notes}
    event_methods = (('-OPEN', 'open'),
                     ('-SHOW', 'show'),
                     ('-MOVE', 'move'),
                     ('-DELETE', 'delete'))
    for event_prefix, method_name in event_methods:
        if event.startswith(event_prefix):
            call_note_listbox_method(method_name,
                                     selected_titles,
                                     listbox_notes_dict,
                                     listbox_notes)
            break


def call_note_listbox_method(method_name: str,
                             titles: List[str],
                             listbox_notes_dict: Dict[str, Note],
                             listbox_notes: List[Note]) -> None:
    """Calls a method on a note in a listbox.

    Assumes that the method name is valid.

    Parameters
    ----------
    method_name : str
        The name of the method to call.
    titles : List[str]
        The titles of the notes to call the method on.
    listbox_notes_dict : dict
        A dictionary mapping note titles to notes.
    listbox_notes : List[Note]
        The notes displayed in the listbox.
    """
    for title in titles:
        note_: Note = listbox_notes_dict[title]
        method = getattr(note_, method_name)
        if method() is None:
            listbox_notes.remove(note_)


if __name__ == '__main__':
    sg.theme('TanBlue')
    main()

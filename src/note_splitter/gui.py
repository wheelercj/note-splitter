import PySimpleGUI as sg

"""
    PySimpleGUI Note Splitter Demo Program Project GUI

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

def make_window(theme):
    sg.theme(theme)
    menu_def = [['&Close Application', ['E&xit']],
                ['&Help', ['&Documentation']] ]
    right_click_menu_def = [[], ['Versions', 'Clear Screen', 'Exit']]

    frame_layout = [[sg.T('Split by:')],
                  [sg.CB('Check 1'), sg.CB('Check 2'), sg.CB('Check 3')]]

    input_layout =  [

                # [sg.Menu(menu_def, key='-MENU-')],

                [sg.Multiline('Note Splitter User Tips:\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nYou get the point.', size=(45,5), expand_x=True, expand_y=True, k='-MLINE-')],

                [sg.Text("Add a file: "), sg.Input(key="-IN2-",change_submits=True), sg.FilesBrowse(key="-IN-")],

                [sg.Frame('', frame_layout, font='Any 12', title_color='blue')],

                # [sg.Checkbox('Checkbox', default=True, k='-CB-')],
                # [sg.Radio('Radio1', "RadioDemo", default=True, size=(10,1), k='-R1-'), sg.Radio('Radio2', "RadioDemo", default=True, size=(10,1), k='-R2-')],

                [sg.Combo(values=('Combo 1', 'Combo 2', 'Combo 3'), default_value='Combo 1', readonly=True, k='-COMBO-'),

                 sg.OptionMenu(values=('Option 1', 'Option 2', 'Option 3'),  k='-OPTION MENU-'),],

                [sg.Button('Split'), sg.Button('Split Summary')]]

    logging_layout = [[sg.Text("Anything printed will display here!")],
                      [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                      # [sg.Output(size=(60,15), font='Courier 8', expand_x=True, expand_y=True)]
                      ]

    specialty_layout = [[sg.Text("Any \"special\" elements will display here!")],
                      [sg.Button("Open Folder")],
                      [sg.Button("Open File")]]

    settings_layout = [[sg.Text("Any \"setting\" changes will be chosen and displayed here!")]]
    
    theme_layout = [[sg.Text("Change the theme of Note Splitter to your liking!")],
                    [sg.Listbox(values = sg.theme_list(), 
                      size =(20, 12), 
                      key ='-THEME LISTBOX-',
                      enable_events = True)],
                      [sg.Button("Set Theme")]]
    
    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
                [sg.Text('Note Splitter', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    layout +=[[sg.TabGroup([[  sg.Tab('Home', input_layout),
                               sg.Tab('Dummy Tab', specialty_layout),
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

def popup_folderbrowse(message: str) -> str:
    """Displays a popup requesting the user to choose a folder.
    
    If the user clicks the Cancel button, an empty string will be 
    returned and the program should cancel splitting.

    Parameters
    ----------
    message : str
        The message to display in the popup.

    Returns
    -------
    str
        The absolute path to the folder the user chose.
    """
    event = None
    while event is None:
        layout = [[sg.Text(message)],
            [sg.FolderBrowse(), sg.InputText()],
            [sg.Submit(), sg.Cancel()]]
        window = sg.Window('Choose a folder', layout)
        event, values = window.read()
    window.close()
    return values[0]

if __name__ == '__main__':
    # sg.theme('black')
    # sg.theme('dark red')
    # sg.theme('dark green 7')
    # sg.theme('DefaultNoMoreNagging')
    sg.theme('TanBlue')
    main()

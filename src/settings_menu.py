# Internal imports
from settings import *

# External imports
import PySimpleGUI as sg
from tkinter.filedialog import askdirectory


# Load the settings or get them from the user if they
# haven't been chosen yet, and return the settings.
def get_settings():
    if os.path.exists('user_settings.yaml'):
        return load_settings()
    else:
        return settings_menu()


# Display a menu for the user to choose settings.
def settings_menu():
    if os.path.exists('user_settings.yaml'):
        settings = load_settings()
        zk_paths = settings.get_zettelkasten_paths()
        ad_paths = settings.get_asset_dir_paths()
        dl_paths = settings.get_downloads_paths()
    else:
        zk_paths = []
        ad_paths = []
        dl_paths = []

    window = create_settings_menu(zk_paths, ad_paths, dl_paths)

    while True:
        event, values = window.read()

        # If the user clicks 'Save'.
        if event == 'Save':
            window.close()
            settings = Settings(zk_paths, ad_paths, dl_paths)
            save_settings(settings)
            return settings

        # If the user closes the window or clicks 'Cancel'.
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            return

        zk_paths, ad_paths, dl_paths = respond_to_menu_event(event, values, window, zk_paths, ad_paths, dl_paths)


def create_settings_menu(zk_paths, ad_paths, dl_paths):
    asset_types_str = get_asset_types_str()

    zk_tab_layout = [[sg.Text('Choose the folder(s) where you save your zettels.')],
                     [sg.Listbox(zk_paths, size=(100, 6), key='-zk_paths-')],
                     [sg.Button('New', key='-zk_new-'), sg.Button('Edit', key='-zk_edit-'), sg.Button('Delete', key='-zk_delete-')]]

    ad_tab_layout = [[sg.Text(f'Choose any folders where all the files of types {asset_types_str} are linked to in the zettelkasten.'
                              '\nThe top folder is the default folder that assets can be automatically moved to.')],
                     [sg.Listbox(ad_paths, size=(100, 6), key='-ad_paths-')],
                     [sg.Button('New', key='-ad_new-'), sg.Button('Edit', key='-ad_edit-'), sg.Button('Delete', key='-ad_delete-'), sg.Button('Move to top', key='-ad_move_to_top-')]]

    dl_tab_layout = [[sg.Text('Optionally choose folders to automatically move linked assets from.'
                              f'\nAny of these linked assets that are of type {asset_types_str} will be moved to the'
                              '\ntop chosen assets folder, and their links in the zettels will be updated.')],
                     [sg.Listbox(dl_paths, size=(100, 6), key='-dl_paths-')],
                     [sg.Button('New', key='-dl_new-'), sg.Button('Edit', key='-dl_edit-'), sg.Button('Delete', key='-dl_delete-')]]

    layout = [[sg.TabGroup([[sg.Tab('Zettelkasten folders', zk_tab_layout),
                             sg.Tab('Assets folders', ad_tab_layout),
                             sg.Tab('Downloads folders', dl_tab_layout)]])],
              [sg.Save(), sg.Cancel()]]

    return sg.Window('Zettelkasten settings', layout)


def respond_to_menu_event(event, values, window, zk_paths, ad_paths, dl_paths):
    # Respond to zettelkasten directory button events.
    if event == '-zk_new-':
        # Append a new zettelkasten directory.
        new_path = askdirectory(title='Select the zettelkasten folder.', mustexist=True)
        if new_path != '':
            zk_paths.append(new_path)
            window['-zk_paths-'].update(zk_paths)
    elif event == '-zk_edit-':
        # Edit a previously chosen zettelkasten directory.
        if len(values['-zk_paths-']) == 0:
            sg.Popup('Please select a folder to edit in the list', title='Error')
        else:
            new_path = askdirectory(title='Select the zettelkasten folder.', mustexist=True)
            if new_path != '':
                # Replace the instances of values['-zk_paths-'][0] in zk_paths with the new path.
                zk_paths = [new_path if path == values['-zk_paths-'][0] else path for path in zk_paths]
                window['-zk_paths-'].update(zk_paths)
    elif event == '-zk_delete-':
        # Delete a previously chosen zettelkasten directory.
        if len(values['-zk_paths-']) == 0:
            sg.Popup('Please select a folder to delete in the list', title='Error')
        else:
            zk_paths.remove(values['-zk_paths-'][0])
            window['-zk_paths-'].update(zk_paths)

    # Respond to asset directory button events.
    elif event == '-ad_new-':
        # Append a new assets directory.
        new_path = askdirectory(title='Select the assets folder.', mustexist=True)
        if new_path != '':
            ad_paths.append(new_path)
            window['-ad_paths-'].update(ad_paths)
    elif event == '-ad_edit-':
        # Edit a previously chosen assets directory.
        if len(values['-ad_paths-']) == 0:
            sg.Popup('Please select a folder to edit in the list', title='Error')
        else:
            new_path = askdirectory(title='Select the assets folder.', mustexist=True)
            if new_path != '':
                # Replace the instances of values['-ad_paths-'][0] in ad_paths with the new path.
                ad_paths = [new_path if path == values['-ad_paths-'][0] else path for path in ad_paths]
                window['-ad_paths-'].update(ad_paths)
    elif event == '-ad_delete-':
        # Delete a previously chosen assets directory.
        if len(values['-ad_paths-']) == 0:
            sg.Popup('Please select a folder to delete in the list', title='Error')
        else:
            ad_paths.remove(values['-ad_paths-'][0])
            window['-ad_paths-'].update(ad_paths)
    elif event == '-ad_move_to_top-':
        # Move the selected assets directory to the top of the list.
        if len(values['-ad_paths-']) == 0:
            sg.Popup('Please select a folder to move in the list', title='Error')
        else:
            ad_paths.remove(values['-ad_paths-'][0])
            ad_paths.insert(0, values['-ad_paths-'][0])
            window['-ad_paths-'].update(ad_paths)

    # Respond to downloads directory button events.
    elif event == '-dl_new-':
        # Append a new downloads directory.
        new_path = askdirectory(title='Select the downloads folder.', mustexist=True)
        if new_path != '':
            dl_paths.append(new_path)
            window['-dl_paths-'].update(dl_paths)
    elif event == '-dl_edit-':
        # Edit a previously chosen downloads directory.
        if len(values['-dl_paths-']) == 0:
            sg.Popup('Please select a folder to edit in the list', title='Error')
        else:
            new_path = askdirectory(title='Select the downloads folder.', mustexist=True)
            if new_path != '':
                # Replace the instances of values['-dl_paths-'][0] in dl_paths with the new path.
                dl_paths = [new_path if path == values['-dl_paths-'][0] else path for path in dl_paths]
                window['-dl_paths-'].update(dl_paths)
    elif event == '-dl_delete-':
        # Delete a previously chosen downloads directory.
        if len(values['-dl_paths-']) == 0:
            sg.Popup('Please select a folder to delete in the list', title='Error')
        else:
            dl_paths.remove(values['-dl_paths-'][0])
            window['-dl_paths-'].update(dl_paths)

    return zk_paths, ad_paths, dl_paths


if __name__ == '__main__':
    settings_menu()
    # Using yaml.dump in __main__ causes the yaml python object to
    # have the wrong name, so fix the name in the yaml file.
    with open('user_settings.yaml', 'r') as file:
        contents = file.read()
    contents = contents.replace('__main__', 'settings', 1)
    with open('user_settings.yaml', 'w') as file:
        file.write(contents)

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
# Return the settings.
def settings_menu():
    if os.path.exists('user_settings.yaml'):
        settings = load_settings()
    else:
        settings = default_settings()

    window = create_settings_menu(settings)

    while True:
        event, values = window.read()

        if event == 'Save':
            window.close()
            save_settings(settings)
            return settings
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            return settings

        settings = respond_to_menu_event(event, values, window, settings)


def create_settings_menu(settings):
    asset_types_str = get_asset_types_str()

    zk_tab_layout = [[sg.Text('Choose the folder(s) where you save your zettels.')],
                     [sg.Listbox(settings['zk_paths'], size=(100, 6), key='-zk_paths-')],
                     [sg.Button('New', key='-zk_new-'), sg.Button('Edit', key='-zk_edit-'), sg.Button('Delete', key='-zk_delete-')]]

    ad_tab_layout = [[sg.Text(f'Choose any folders where all the files of types {asset_types_str} are linked to in the zettelkasten.'
                              '\nThe top folder is the default folder that assets can be automatically moved to.')],
                     [sg.Listbox(settings['ad_paths'], size=(100, 6), key='-ad_paths-')],
                     [sg.Button('New', key='-ad_new-'), sg.Button('Edit', key='-ad_edit-'), sg.Button('Delete', key='-ad_delete-'), sg.Button('Move to top', key='-ad_move_to_top-')]]

    dl_tab_layout = [[sg.Text('Optionally choose folders to automatically move linked assets from.'
                              f'\nAny of these linked assets that are of type {asset_types_str} will be moved to the'
                              '\ntop chosen assets folder, and their links in the zettels will be updated.')],
                     [sg.Listbox(settings['dl_paths'], size=(100, 6), key='-dl_paths-')],
                     [sg.Button('New', key='-dl_new-'), sg.Button('Edit', key='-dl_edit-'), sg.Button('Delete', key='-dl_delete-')]]

    layout = [[sg.TabGroup([[sg.Tab('Zettelkasten folders', zk_tab_layout),
                             sg.Tab('Assets folders', ad_tab_layout),
                             sg.Tab('Downloads folders', dl_tab_layout)]])],
              [sg.Save(), sg.Cancel()]]

    return sg.Window('Zettelkasten settings', layout)


def respond_to_menu_event(event, values, window, settings):
    if event == '-ad_move_to_top-':
        # Move the selected assets directory to the top of the list.
        if len(values['-ad_paths-']) == 0:
            sg.Popup('Please select a folder to move in the list', title='Error')
        else:
            settings['ad_paths'].remove(values['-ad_paths-'][0])
            settings['ad_paths'].insert(0, values['-ad_paths-'][0])
            window['-ad_paths-'].update(settings['ad_paths'])

    elif event.endswith('_new-'):
        settings = new_dir_setting(event[1:3], values, window, settings)
    elif event.endswith('_edit-'):
        settings = edit_dir_setting(event[1:3], values, window, settings)
    elif event.endswith('_delete-'):
        settings = delete_dir_setting(event[1:3], values, window, settings)

    return settings


def new_dir_setting(dir_type, values, window, settings):
    # Append a new directory.
    new_path = askdirectory(title='Select the folder.', mustexist=True)
    if new_path != '':
        settings[f'{dir_type}_paths'].append(new_path)
        window[f'-{dir_type}_paths-'].update(settings[f'{dir_type}_paths'])

    return settings


def edit_dir_setting(dir_type, values, window, settings):
    # Edit a previously chosen directory.
    if len(values[f'-{dir_type}_paths-']) == 0:
        sg.Popup('Please select a folder to edit in the list', title='Error')
    else:
        new_path = askdirectory(title='Select the folder.', mustexist=True)
        if new_path != '':
            # Replace the instances of the old path with the new path.
            settings[f'{dir_type}_paths'] = [new_path if path == values[f'-{dir_type}_paths-'][0] else path for path in settings[f'{dir_type}_paths']]
            window[f'-{dir_type}_paths-'].update(settings[f'{dir_type}_paths'])

    return settings


def delete_dir_setting(dir_type, values, window, settings):
    # Delete a previously chosen directory.
    if len(values[f'-{dir_type}_paths-']) == 0:
        sg.Popup('Please select a folder to delete in the list', title='Error')
    else:
        settings[f'{dir_type}_paths'].remove(values[f'-{dir_type}_paths-'][0])
        window[f'-{dir_type}_paths-'].update(settings[f'{dir_type}_paths'])

    return settings


if __name__ == '__main__':
    settings_menu()

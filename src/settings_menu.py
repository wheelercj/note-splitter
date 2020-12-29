# External imports
import os
import re
import yaml
import PySimpleGUI as sg
from tkinter.filedialog import askdirectory


'''
To add support for a new asset type to the program, change:
* asset_types (below)
* asset_link_pattern (below)
* the list of supported file types in the README
'''
zettel_types = ('.md')  # Changing zettel_types will require changes in several other places if the new zettel type has a different length.
zettel_id_pattern = re.compile(r'(?<!\[\[)\d{14}(?!]])')
asset_types = ('.html', '.jpeg', '.jpg', '.m4a', '.mp4', '.pdf', '.png')
asset_link_pattern = re.compile(r'(?<=]\()(?!https?://|www\d?\.|mailto:|zotero:|obsidian:)(?P<link>.*?(?P<name>[^(/|\\)]*?(\.(html|jpeg|jpg|m4a|mp4|pdf|png))))(?=\))')
web_types = ('.ac', '.ad', '.ae', '.aero', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.arpa', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.biz', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cat', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.com', '.coop', '.cr', '.cs', '.cu', '.cv', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.edu', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.firm', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gov', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', '.in', '.info', '.int', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jobs', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.mg', '.mh', '.mil', '.mk', '.ml', '.mm', '.mn', '.mo', '.mobi', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.museum', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.name', '.nato', '.nc', '.ne', '.net', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.org', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.pro', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.store', '.sv', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.travel', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.web', '.wf', '.ws', '.ye', '.yt', '.yu', '.za', '.zm', '.zw')


# Load the settings or get them from the user if they
# haven't been chosen yet, and return the settings.
def get_settings():
    if os.path.exists('user_settings.yaml'):
        return load_settings()
    else:
        return settings_menu()


def load_settings():
    with open('user_settings.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def save_settings(settings):
    with open('user_settings.yaml', 'w') as file:
        yaml.dump(settings, file)


# Return a dict of the default settings.
def default_settings():
    settings = dict()
    settings['zk_paths'] = []  # Zettelkasten paths.
    settings['ad_paths'] = []  # Asset directory paths.
    settings['dl_paths'] = []  # Downloads paths.

    return settings


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
        settings = new_dir_setting(f'{event[1:3]}_paths', values, window, settings)
    elif event.endswith('_edit-'):
        settings = edit_dir_setting(f'{event[1:3]}_paths', values, window, settings)
    elif event.endswith('_delete-'):
        settings = delete_dir_setting(f'{event[1:3]}_paths', values, window, settings)

    return settings


# Append a new directory.
def new_dir_setting(paths_type, values, window, settings):
    new_path = askdirectory(title='Select the folder.', mustexist=True)
    if new_path != '':
        settings[paths_type].append(new_path)
        window[f'-{paths_type}-'].update(settings[paths_type])

    return settings


# Edit a previously chosen directory.
def edit_dir_setting(paths_type, values, window, settings):
    if len(values[f'-{paths_type}-']) == 0:
        sg.Popup('Please select a folder to edit in the list', title='Error')
    else:
        new_path = askdirectory(title='Select the folder.', mustexist=True)
        if new_path != '':
            # Replace the instances of the old path with the new path.
            settings[paths_type] = [new_path if path == values[f'-{paths_type}-'][0] else path for path in settings[paths_type]]
            window[f'-{paths_type}-'].update(settings[paths_type])

    return settings


# Delete a previously chosen directory.
def delete_dir_setting(paths_type, values, window, settings):
    if len(values[f'-{paths_type}-']) == 0:
        sg.Popup('Please select a folder to delete in the list', title='Error')
    else:
        settings[paths_type].remove(values[f'-{paths_type}-'][0])
        window[f'-{paths_type}-'].update(settings[paths_type])

    return settings


# Convert the tuple of asset types into a readable sentence.
def get_asset_types_str():
    asset_types_list = []
    for asset_type in asset_types:
        asset_types_list.append(asset_type[1:])
    asset_types_str = ', '.join(asset_types_list)
    split_types = asset_types_str.rsplit(', ', 1)
    asset_types_str = split_types[0] + ', and ' + split_types[1]

    return asset_types_str


# Check whether all the filepaths in the given list are absolute.
def all_abs(paths):
    for path in paths:
        if not path == '' and not os.path.isabs(path):
            return False
    return True


if __name__ == '__main__':
    settings_menu()

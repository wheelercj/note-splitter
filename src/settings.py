# Settings for the locations of the zettelkasten, its assets, and any
# downloads folders to automatically move assets from. Any linked
# assets in a downloads folder are automatically moved to whichever
# assets folder was chosen first. Choosing a downloads folder is
# optional. Running this program directly will let you overwrite any
# settings you had already chosen.

# External imports
import os
import sys
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


class Settings:
    def __init__(self, zettelkasten_paths, asset_dir_paths, downloads_paths):
        # Make sure all the paths are absolute.
        if not all_abs(zettelkasten_paths + asset_dir_paths + downloads_paths):
            sg.Popup(f'In the zettelkasten settings in user_settings.yaml, all the folder paths must be absolute.', title='Error')
            sys.exit(0)

        self.__zettelkasten_paths = zettelkasten_paths
        self.__asset_dir_paths = asset_dir_paths
        self.__downloads_paths = downloads_paths

    def get_zettelkasten_paths(self):
        return self.__zettelkasten_paths

    def get_asset_dir_paths(self):
        return self.__asset_dir_paths

    def get_downloads_paths(self):
        return self.__downloads_paths


# Check whether all the filepaths in the given list are absolute.
def all_abs(paths):
    for path in paths:
        if not path == '' and not os.path.isabs(path):
            return False
    return True


# Load the settings or get them from the user if they
# haven't been chosen yet, and return the settings.
def get_settings():
    if os.path.exists('user_settings.yaml'):
        return load_settings()
    else:
        return choose_settings()


# Display a menu for the user to choose settings.
def choose_settings():
    if os.path.exists('user_settings.yaml'):
        settings = load_settings()
        zk_paths = settings.get_zettelkasten_paths()
        ad_paths = settings.get_asset_dir_paths()
        dl_paths = settings.get_downloads_paths()
    else:
        zk_paths = []
        ad_paths = []
        dl_paths = []

    layout = create_menu_layout(zk_paths, ad_paths, dl_paths)
    window = sg.Window('Zettelkasten settings', layout)

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


# Convert the tuple of asset types into a readable sentence.
def get_asset_types_str():
    asset_types_list = []
    for asset_type in asset_types:
        asset_types_list.append(asset_type[1:])
    return ', '.join(asset_types_list)


def load_settings():
    # If this function is being called with settings.py == '__main__',
    # the yaml file must have a python yaml object name of '__main__'.
    if __name__ == '__main__':
        with open('user_settings.yaml', 'r') as file:
            contents = file.read()
        contents = contents.replace('settings', '__main__', 1)
        with open('user_settings.yaml', 'w') as file:
            file.write(contents)

    with open('user_settings.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


# Save the settings chosen by the user to user_settings.yaml.
def save_settings(settings):
    with open('user_settings.yaml', 'w') as file:
        yaml.dump(settings, file)
    # If there are square brackets anywhere in the file, that's supposed to
    # be an empty list but it won't be read correctly by yaml.load, so change
    # all instances of ' []' with '\n- \'\''
    with open('user_settings.yaml', 'r') as file:
        contents = file.read()
    contents = contents.replace(' []', '\n- \'\'')
    with open('user_settings.yaml', 'w') as file:
        file.write(contents)


def create_menu_layout(zk_paths, ad_paths, dl_paths):
    sg.theme('Dark Blue 3')
    asset_types_str = get_asset_types_str()

    zk_tab_layout = [[sg.Text('Choose the folder(s) where you save your zettels.')],
                     [sg.Listbox(values=zk_paths, size=(100, 6), key='-zk_paths-')],
                     [sg.Button('New', key='-zk_new-'), sg.Button('Edit', key='-zk_edit-'), sg.Button('Delete', key='-zk_delete-')]]

    ad_tab_layout = [[sg.Text(f'Choose any folders where all the files of types {asset_types_str} are linked to in the zettelkasten.'
                              '\nThe top folder is the default folder that assets can be automatically moved to.')],
                     [sg.Listbox(values=ad_paths, size=(100, 6), key='-ad_paths-')],
                     [sg.Button('New', key='-ad_new-'), sg.Button('Edit', key='-ad_edit-'), sg.Button('Delete', key='-ad_delete-'), sg.Button('Move to top', key='-ad_move_to_top-')]]

    dl_tab_layout = [[sg.Text('Optionally choose folders to automatically move linked assets from. When you run \'check media\','
                              f'\nany of these linked assets that are of type {asset_types_str} will be moved to the'
                              '\ntop chosen assets folder, and their links in the zettels will be updated.')],
                     [sg.Listbox(values=dl_paths, size=(100, 6), key='-dl_paths-')],
                     [sg.Button('New', key='-dl_new-'), sg.Button('Edit', key='-dl_edit-'), sg.Button('Delete', key='-dl_delete-')]]

    layout = [[sg.TabGroup([[sg.Tab('Zettelkasten folders', zk_tab_layout),
                             sg.Tab('Assets folders', ad_tab_layout),
                             sg.Tab('Downloads folders', dl_tab_layout)]])],
              [sg.Save(), sg.Cancel()]]

    return layout


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
    choose_settings()
    # Using yaml.dump in __main__ causes the yaml python object to
    # have the wrong name, so fix the name in the yaml file.
    with open('user_settings.yaml', 'r') as file:
        contents = file.read()
    contents = contents.replace('__main__', 'settings', 1)
    with open('user_settings.yaml', 'w') as file:
        file.write(contents)

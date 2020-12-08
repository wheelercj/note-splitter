# Settings for the locations of the zettelkasten, its assets, and any
# downloads folders to automatically move assets from. Any linked
# assets in a downloads folder are automatically moved to whichever
# assets folder was chosen first. Choosing a downloads folder is
# optional. Running this program directly will let you overwrite any
# settings you had already chosen.

import os
import sys
import yaml
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter import messagebox


class Settings:
    def __init__(self, zettelkasten_paths, asset_dir_paths, downloads_paths):
        # Make sure all the paths are absolute.
        if not all_abs(zettelkasten_paths + asset_dir_paths + downloads_paths):
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
        if not os.path.isabs(path):
            print('Please make any relative folder paths absolute.')
            return False
    return True


# Load the settings or get them from the user if they
# haven't been chosen yet, and return the settings.
def get_settings():
    # Load the settings from the YAML file.
    if os.path.exists('user_settings.yaml'):
        with open('user_settings.yaml', 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    else:  # The settings haven't been chosen yet.
        settings = choose_settings()
        update_user_settings_yaml(settings)
        return settings


# Ask the user to choose all the settings.
def choose_settings():
    Tk().withdraw()
    print(f'Select the zettelkasten folder(s).')
    zettelkasten_paths = select_folder_paths('zettelkasten')
    print(f'Select the assets folder(s).')
    asset_dir_paths = select_folder_paths('assets')
    print(f'Select the downloads folder(s).')
    downloads_paths = select_folder_paths('downloads')

    return Settings(zettelkasten_paths, asset_dir_paths, downloads_paths)


# Ask the user to select folders.
def select_folder_paths(folder_type):
    folder_paths = []
    messagebox.showinfo(title='Zettelkasten settings', message=f'Select the {folder_type} folder(s). Click \'Cancel\' when finished.')

    while True:
        path = askdirectory(title=f'Select the {folder_type} folder.', mustexist=True)
        if path == '':
            break
        folder_paths.append(path)

    return folder_paths


# Save the settings chosen by the user to user_settings.yaml.
def update_user_settings_yaml(settings):
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


if __name__ == '__main__':
    update_user_settings_yaml(choose_settings())
    # Using yaml.dump in __main__ causes the yaml python object to
    # have the wrong name, so fix the name in the yaml file.
    with open('user_settings.yaml', 'r') as file:
        contents = file.read()
    contents = contents.replace('__main__', 'settings', 1)
    with open('user_settings.yaml', 'w') as file:
        file.write(contents)
else:
    settings = get_settings()

# This program can move files of all types, and any files that are of type
# asset_types that are linked to in the zettelkasten will have their links updated.
# Any zettels moved will have their relative links updated as well.

# Internal imports
try:
    from common import *
    from links import format_link
    from settings_menu import get_settings
except ModuleNotFoundError:
    from .common import *
    from .links import format_link
    from .settings_menu import get_settings

# External imports
import os
import sys
from collections import Counter
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory
import PySimpleGUI as sg


# Get input from the user about which files to move where,
# move the files, and update any file links that need updating.
def move_files_main():
    Tk().withdraw()
    chosen_paths = get_paths_to_move()
    all_zettel_paths = get_zettel_paths()
    all_asset_links = get_all_asset_links(all_zettel_paths)
    chosen_paths = categorize_chosen_paths(chosen_paths, all_asset_links)
    chosen_paths = confirm_move_categories(chosen_paths)

    print('\nSelect the destination folder.')
    destination = askdirectory(title='Select the destination folder.', mustexist=True)
    print(f'Selected folder {destination}')

    changed_link_count = update_zettelkasten_links(chosen_paths, destination, all_zettel_paths)
    moved_file_count = move_files(chosen_paths, destination)

    # Print a summary of what the program did.
    print(f'\nMoved {moved_file_count} files to folder '
          f'\n{os.path.split(destination)[-1]}'
          f'\n and updated {changed_link_count} links.\n')


# Get input of paths of files to move.
def get_paths_to_move():
    print('Select the files you want to move.')
    chosen_paths = askopenfilenames(title='Select the files you want to move.')
    if len(chosen_paths):
        print('Selected files:')
        for chosen_path in chosen_paths:
            print(f'   {chosen_path}')
    else:
        print('No files selected.\n')
        sys.exit(0)

    return chosen_paths


# Return a dict of lists.
# Parameter chosen_filepaths is a list of formatted paths.
# Parameter all_asset_links is a Links object.
def categorize_chosen_paths(chosen_filepaths, all_asset_links):
    categories = dict()
    categories['zettel_paths'] = []     # All filepaths that are of a type in zettel_types and are in settings.zettelkasten_paths.
    categories['nonzettel_paths'] = []  # All filepaths that are of a type in zettel_types, but are not in settings.zettelkasten_paths.
    categories['asset_paths'] = []      # All filepaths that are of a type in asset_types and are linked to in the zettels.
    categories['nonasset_paths'] = []   # All filepaths that are of a type in asset_types, but are not linked to.
    categories['other_paths'] = []      # All other filepaths that don't fit in any above category.

    settings = get_settings()

    for filepath in chosen_filepaths:
        folder = os.path.split(filepath)[0]
        ext = os.path.splitext(filepath)[1]

        if ext in zettel_types:
            if folder in settings['zettelkasten_paths']:
                categories['zettel_paths'].append(filepath)
            else:
                categories['nonzettel_paths'].append(filepath)
        elif ext in asset_types:
            if filepath in all_asset_links.formatted:
                categories['asset_paths'].append(filepath)
            else:
                categories['nonasset_paths'].append(filepath)
        else:
            categories['other_paths'].append(filepath)

    return categories


def confirm_move_categories(chosen_paths):
    if len(chosen_paths['nonzettel_paths']) > 0:
        answer = sg.PopupYesNo('Some of the chosen markdown files are not in any '
                               'zettelkasten folders chosen in settings, and will '
                               'not have any relative file links kept up to date.'
                               '\n' + chosen_paths['nonzettel_paths'] + '\n'
                               'Would you like to move them anyways?')
        if answer == 'No':
            del chosen_paths['nonzettel_paths']

    if len(chosen_paths['nonasset_paths']) > 0:
        answer = sg.PopupYesNo('Some of the chosen files do not appear to be '
                               'linked to in the zettelkasten.'
                               '\n' + chosen_paths['nonasset_paths'] + '\n'
                               'Would you like to move them anyways?')
        if answer == 'No':
            del chosen_paths['nonasset_paths']

    if len(chosen_paths['other_paths']) > 0:
        answer = sg.PopupYesNo('Some of the chosen files are of types not fully '
                               'supported by this program, so any file links in '
                               'the zettelkasten cannot be updated.'
                               '\n' + chosen_paths['other_paths'] + '\n'
                               'Would you like to move them anyways?')
        if answer == 'No':
            del chosen_paths['other_paths']

    if len(chosen_paths) == 0:
        print('No files remain.')
        sys.exit(0)

    return chosen_paths


def update_zettelkasten_links(chosen_paths, destination, all_zettel_paths):
    changed_link_count = 0

    print('\nUpdating links in the zettelkasten.')
    for zettel_path in all_zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        changed_link_count += update_asset_links(chosen_paths, destination, zettel_path, contents)

    return changed_link_count


def update_asset_links(chosen_paths, destination, zettel_path, zettel_contents):
    # Get all the links in this zettel as a Links object.
    Links_in_zettel = get_asset_links(zettel_contents, zettel_path)

    # The lists in the Links_in_zettel object may contain duplicates, so
    # get a dict of each unique link and their number of occurences.
    formatted_links_counter = Counter(Links_in_zettel.formatted)

    # If this zettel is being moved, make any relative links in it absolute.
    if zettel_path in chosen_paths['zettel_paths']:
        zettel_contents = absolutize_links(Links_in_zettel, zettel_contents)

    for chosen_path in chosen_paths:  # TODO: use chosen_paths as a dict
        # Get the number of links to change by finding chosen_path in formatted_links_counter.
        try:
            link_count = formatted_links_counter[chosen_path]
        except KeyError:
            link_count = 0
        if link_count:
            # Update the link in the zettel's contents.
            zettel_contents, link_in_zettel, new_link = update_asset_link(chosen_path, destination, zettel_path, Links_in_zettel)

            # Save the changed contents.
            with open(zettel_path, 'w', encoding='utf8') as zettel:
                zettel.write(zettel_contents)

            zettel_link = get_zettel_link(zettel_path)
            print(f'   Changed \'{link_in_zettel}\'')
            print(f'      to \'{new_link}\'')
            print(f'      in {zettel_link}')

    return link_count


# Replace all instances of the link in the zettel's contents with
# a new link that is in the destination folder.
# Return the updated contents without saving them.
def update_asset_link(chosen_path, destination, zettel_path, Links_in_zettel):
    # The link in the zettel is chosen_path, except not necessarily formatted,
    # so we need to get its original form from the Links_in_zettel object.
    index = Links_in_zettel.formatted.index(chosen_path)
    link_in_zettel = Links_in_zettel.originals[index]

    # Create the new_link that the current (old) link will be changed to.
    asset_name = os.path.split(link_in_zettel)[-1]
    new_link = os.path.join(destination, asset_name)
    new_link = format_link(new_link, zettel_path)

    # Update the zettel_contents with the new_link.
    zettel_contents = zettel_contents.replace(link_in_zettel, new_link)

    return zettel_contents, link_in_zettel, new_link


def absolutize_links(Links_in_zettel, zettel_contents):
    for asset_link in Links_in_zettel:
        if not os.path.isabs(asset_link.original):
            current_link_pattern = re.escape(asset_link.original)
            new_link = asset_link.formatted
            zettel_contents = re.sub(current_link_pattern, new_link, zettel_contents)

    return zettel_contents


# Get info about which files to move where and move the files.
# Parameters:
#   chosen_paths is a dict of lists of the abs paths of files that are to be moved.
#   destination is the abs path of a folder.
def move_files(chosen_paths, destination):
    moved_file_count = 0

    print('\nMoving chosen files.')
    for category in chosen_paths:
        for chosen_path in chosen_paths[category]:
            new_path = os.path.join(destination, os.path.split(chosen_path)[-1])
            new_path = new_path.replace('\\', '/')
            if move_file_or_folder(chosen_path, new_path):
                moved_file_count += 1
            if chosen_path.endswith('.html'):
                if move_html_folder(chosen_path, destination):
                    moved_file_count += 1

    return moved_file_count


# Return a bool for whether the file/folder is successfully moved.
def move_file_or_folder(chosen_path, new_path):
    try:
        os.rename(chosen_path, new_path)
        print(f'   Moved {chosen_path}')
        print(f'      to {new_path}')
        return True
    except FileExistsError:
        print(f'   Unable to move {chosen_path}')
        print(f'      to {new_path}')
        print(f'      because a copy is already there.')
        return False


# Assuming chosen path is an .html file, try to move a corresponding folder too.
# Return a bool for whether the folder is successfully moved.
def move_html_folder(chosen_path, destination):
    folder_path = chosen_path[0:-5] + '_files'
    if os.path.isdir(folder_path):
        folder_name = os.path.split(folder_path)[-1]
        new_path = os.path.join(destination, folder_name)
        if move_file_or_folder(folder_path, new_path):
            return True
    else:
        print(f'Could not find folder \'{folder_path}\'.')

    return False


if __name__ == '__main__':
    move_files_main()

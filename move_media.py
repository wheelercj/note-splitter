# This program can move assets of type asset_types that are linked to in the
# zettelkasten from one folder to another, and updates their links.

# Internal
from common import *
from links import Links, format_link
from settings import settings

# External
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory
from collections import Counter


# Get input from the user about which files to move where, move the files, and update links.
def move_media_main():
    Tk().withdraw()
    zettel_paths = get_zettel_paths()

    # Get input of paths of files to move.
    print('Select the assets you want to move.')
    chosen_paths = askopenfilenames(title='Select the asset files you want to move.')
    print('Selected assets:')
    for chosen_path in chosen_paths:
        print(f'   {chosen_path}')
    if len(chosen_paths) == 0:
        print('   (none)')

    # Keep only files that are of type asset_types and are linked to in the zettelkasten.
    chosen_paths = validate_chosen_paths(chosen_paths, get_all_asset_links(zettel_paths))

    link_count = 0
    destination = ''
    if len(chosen_paths):
        # Get input of destination folder.
        print('\nSelect the destination folder.')
        destination = askdirectory(title='Select the destination folder.', mustexist=True)
        print(f'Selected folder {destination}')

        # Move the files and update the links.
        link_count = move_media(chosen_paths, destination, zettel_paths)

    # Print a summary of what the program did.
    print(f'\nMoved {len(chosen_paths)} assets to folder ', end='', flush=True)
    print(f'\'{os.path.split(destination)[-1]}\' and updated {link_count} links.\n')


# Get parameters about which files to move where, move the files, and update links.
# Parameters:
#   chosen_paths is a list of the absolute paths of asset files that are to be moved. They are linked to.
#   destination is the absolute path of a folder.
#   zettel_paths is a list of paths to all zettels in the zettelkasten.
def move_media(chosen_paths, destination, zettel_paths):
    # Update the file links in the zettelkasten.
    changed_link_count = update_links(chosen_paths, destination, zettel_paths)

    # Move the chosen assets.
    print('\nMoving chosen assets.')
    for chosen_path in chosen_paths:
        new_link = os.path.join(destination, os.path.split(chosen_path)[-1])
        try:
            os.rename(chosen_path, new_link)
            print(f'   Moved file {chosen_path}')
            print(f'      to {new_link}')
        except FileExistsError:
            print(f'   Unable to move file {chosen_path}')
            print(f'      because a copy is already there.')

        # If the chosen path is to a .html file, move the corresponding folder too.
        if chosen_path.endswith('.html'):
            folder_path = chosen_path[0:-5] + '_files'
            if os.path.isdir(folder_path):
                folder_name = os.path.split(folder_path)[-1]
                new_path = os.path.join(destination, folder_name)
                try:
                    os.rename(folder_path, new_path)
                    print(f'   Moved folder {folder_path}')
                    print(f'      to {new_path}')
                except FileExistsError:
                    print(f'   Unable to move folder {folder_path}')
                    print(f'      because a copy is already there.')
            else:
                print(f'Could not find folder \'{folder_path}\'.')

    return changed_link_count


# Return all asset file links in the zettels.
def get_all_asset_links(zettel_paths):
    all_links = Links()

    # For each zettel.
    for zettel_path in zettel_paths:
        # Get the contents of the zettel.
        with open(zettel_path, 'r', encoding='utf8') as file:
            contents = file.read()

        # Get the asset links in the contents and save them
        # with all the other links in the Links object.
        links = get_asset_links(contents, zettel_path)
        all_links.add(links)

        # Move any assets in the downloads folders to the zettelkasten's
        # default assets folder, and update their links in the zettelkasten.
        for link in links.formatted:
            downloads_paths = settings.get_downloads_paths()
            for downloads_path in downloads_paths:
                if downloads_path == os.path.split(link)[:-1]:
                    move_media(list(link), asset_dir_paths[0], zettel_paths)
                    break

    return all_links


# Update the links in the zettelkasten.
def update_links(chosen_paths, destination, zettel_paths):
    total_link_count = 0
    print('\nUpdating links in the zettelkasten.')

    # For each zettel.
    for zettel_path in zettel_paths:

        # Get the contents of the zettel.
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()

        # Get all the links in this zettel as a Links object.
        Links_in_zettel = get_asset_links(contents, zettel_path)

        # The lists in the Links_in_zettel object may contain duplicates, so
        # get a dict of each unique link and their number of occurences.
        formatted_links_counter = Counter(Links_in_zettel.formatted)

        # For each path that the user chose to change.
        for chosen_path in chosen_paths:
            # Get the number of links to change by finding chosen_path in formatted_links_counter.
            try:
                count = formatted_links_counter[chosen_path]
            except KeyError:
                count = 0
            if count:
                # Replace all instances of the link in the zettel with
                # the new_link that points to the destination folder.

                # The link in the zettel is chosen_path, except not necessarily formatted,
                # so we need to get its original form from the Links_in_zettel object.
                index = Links_in_zettel.formatted.index(chosen_path)
                link_in_zettel = Links_in_zettel.originals[index]

                # Create the new_link that the current (old) link will be changed to.
                asset_name = os.path.split(link_in_zettel)[-1]
                new_link = os.path.join(destination, asset_name)
                new_link = format_link(new_link)

                # Update the contents with the new_link.
                contents = contents.replace(link_in_zettel, new_link)
                with open(zettel_path, 'w', encoding='utf8') as zettel:
                    zettel.write(contents)
                total_link_count += count
                zettel_link = get_zettel_link(zettel_path)
                print(f'   Changed \'{link_in_zettel}\'')
                print(f'      to \'{new_link}\'')
                print(f'      in {zettel_link}')

    return total_link_count


# Return the given asset paths that are present in the zettels,
# and are of a type in asset_types.
def validate_chosen_paths(chosen_paths, all_asset_links):
    unlinked = []
    wrong_type_links = []
    valid_links = []

    # Determine which file paths are valid, linked assets.
    for filepath in chosen_paths:
        if os.path.splitext(filepath)[1] not in asset_types:
            wrong_type_links.append(filepath)
        elif filepath not in all_asset_links.formatted:
            unlinked.append(filepath)
        else:
            valid_links.append(filepath)

    # Print any error messages needed.
    if len(wrong_type_links):
        print('\nUnable to move some files because of their type:')
        for file in wrong_type_links:
            print(f'   {os.path.split(file)[-1]}')
    if len(unlinked):
        print('\nUnable to move some files because they are not linked to in the zettelkasten:')
        for file in unlinked:
            print(f'   {os.path.split(file)[-1]}')

    return valid_links


if __name__ == '__main__':
    move_media_main()

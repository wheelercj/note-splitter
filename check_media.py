# Search the zettelkasten folder for unused assets,
# and let the user decide what to do with them.

# To add support for a new asset type to the program,
# change both the asset_types and asset_link_pattern variables
# in the file common.py. Other changes in this file may be necessary,
# depending on how the asset can be automatically opened and closed.

# Internal
from common import get_file_names, asset_link_pattern, web_types

# External
import os
import sys
import re
from send2trash import send2trash
import datetime
import pyautogui


def main():
    try:
        zettel_names, dir_asset_names = get_file_names()
        os.chdir('..')
        asset_links, linked_asset_names = get_asset_links(zettel_names)

        unused_assets = find_unused_assets(dir_asset_names, linked_asset_names)  # A dict of unused asset names and their memory sizes.
        missing_assets = get_broken_asset_links(asset_links)  # A list of broken asset links.

        # Sort the assets by descending value.
        sorted_assets = dict()
        for key, value in sorted(unused_assets.items(), key=by_value, reverse=True):
            sorted_assets[key] = value

        # Print info about the assets.
        if len(missing_assets):
            print('\nMissing assets:')
        for missing_asset in missing_assets:
            print(f'   {missing_asset}')
        print('\nUnused assets:')
        print_assets_dict(sorted_assets)
        total_bytes = sum(sorted_assets.values())
        print(f'\nFound {len(unused_assets)} unused asset(s) taking {format_bytes(total_bytes)} of memory,')
        print(f'and {len(missing_assets)} broken asset link(s).')

        if len(sorted_assets) == 0:
            print()
            return

        print('\nMenu:')
        print('1. Choose what to do with each unused asset individually.')
        print('2. Send all unused assets to the recycle bin.')
        print('3. Exit')
        choice = input('> ')

        if choice == '1':
            validate_unused_assets(sorted_assets)
        elif choice == '2':
            delete_unused_assets(sorted_assets)
        else:
            sys.exit(0)

    except SystemExit:
        pass


# For sorting a dictionary by value with the sorted() function.
def by_value(item):
    return item[1]


# Returns a dict with keys of asset names and values of asset file sizes.
def find_unused_assets(dir_asset_names, linked_asset_names):
    # Find unused assets by comparing the zettelkasten's files and the file links in the zettels.
    unused_assets = dict()
    for dir_asset_name in dir_asset_names:
        if dir_asset_name not in linked_asset_names:
            asset_path = dir_asset_name
            unused_assets[dir_asset_name] = os.path.getsize(asset_path)
            # If the unused asset is an .html file, get the size of the corresponding folder too.
            if dir_asset_name.endswith('.html'):
                unused_assets[dir_asset_name] += get_size(asset_path[0:-5] + '_files')

    return unused_assets


# Returns a list of broken asset links.
def get_broken_asset_links(asset_links):
    broken_links = []
    for asset_link in asset_links:
        if not os.path.exists(asset_link):
            broken_links.append(asset_link)

    return broken_links


# Get the total memory size of an entire folder.
def get_size(start_path='.'):
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Skip the file if it is a symbolic link.
            if not os.path.islink(filepath):
                total_size += os.path.getsize(filepath)

    return total_size


# Returns a list of all asset file links in the zettels.
def get_asset_links(zettel_names):
    # TODO: create asset_links dict so the output can say where the broken links are.
    # asset_links = dict()  # A dict of zettel names and their links.
    asset_links = []
    linked_asset_names = []

    # For each zettel.
    for zettel_name in zettel_names:
        # Find all the links in the zettel.
        with open(zettel_name, 'r', encoding='utf8') as file:
            contents = file.read()
        p = re.compile(asset_link_pattern)
        new_links = p.findall(contents)

        # Append this zettel's links to the list of all links.
        for new_link in new_links:
            link = new_link[0]
            name = new_link[1]

            # Ignore URLs.
            if is_URL(link):
                continue

            # Remove 'file://' from the beginning of any file links that have it.
            if link.startswith('file://'):
                link = link[7:]

            # Make any relative file links absolute.
            link = os.path.abspath(link)

            # Replace all instances of '\' with '/'.
            link = link.replace('\\', '/')

            # Move any assets in the downloads folder to the zettelkasten.
            # if '/Downloads/' in link:
            # TODO: change the link variable
            # move the file
            # update the zettel

            # Append the link to the list of all links.
            asset_links.append(link)
            linked_asset_names.append(name)

    return asset_links, linked_asset_names


def is_URL(link):
    for web_type in web_types:
        if web_type in link:
            return True
    return False


# Print the names and the bytes of each asset.
def print_assets_dict(assets_dict):
    if len(assets_dict) == 0:
        return
    name_size = len(max(assets_dict.keys(), key=len))  # The size of the longest asset name.
    for key, value in assets_dict.items():
        Bytes = format_bytes(value)
        print(f'   {key:<{name_size}}{Bytes:>12}')


# Convert bytes to kilobytes, megabytes, etc.
# Returns a string of the converted bytes with the appropriate units.
def format_bytes(Bytes):
    power = 0
    while Bytes > 1024:
        power += 3
        Bytes /= 1024
    result = '{:.2f}'.format(round(Bytes, 2))
    if power == 0:
        return result + '  B'
    elif power == 3:
        return result + ' kB'
    elif power == 6:
        return result + ' MB'
    elif power == 9:
        return result + ' GB'
    elif power == 12:
        return result + ' TB'
    else:
        raise ValueError('File size not yet supported.')


# For each asset:
#   open the asset
#   ask the user what to do with it
def validate_unused_assets(unused_assets):
    print('\nChoose what to do with each unused asset.')
    print('You can enter q to quit.\n')
    for key, value in unused_assets.items():
        # Print the asset name and memory.
        Bytes = format_bytes(value)
        print(f'{key}{Bytes:>10}')

        # Open the asset for the user to view.
        os.startfile(key)
        pyautogui.sleep(0.5)
        asset_window = pyautogui.getActiveWindow()
        # Bring the program's window back to the front.
        pyautogui.hotkey('alt', 'tab')
        choice = input('Send asset to the recycle bin? [y/n]: ')
        # Close the asset window.
        if key.endswith('.html'):
            pyautogui.hotkey('alt', 'tab')
            pyautogui.hotkey('ctrl', 'w')
            pyautogui.hotkey('alt', 'tab')
        else:
            asset_window.close()

        # Respond to the user's choice.
        if choice == 'y':
            send2trash(key)
            # If the asset is an .html file, move the corresponding folder.
            if key.endswith('.html'):
                folder_name = key[0:-5] + '_files'
                if os.path.isdir(folder_name):
                    try:
                        send2trash(folder_name)
                    except OSError:
                        print('OSError')
                else:
                    print(f'Could not find folder \'{folder_name}\'.')
            print('Asset sent to the recycle bin.\n')
        elif choice == 'n':
            print('Asset saved.\n')
        elif choice == 'q':
            sys.exit(0)
        else:
            print('Asset saved.\n')

    print('\nAll assets validated.\n')


# Send all unused assets to the recycle bin in a new folder.
def delete_unused_assets(unused_assets):
    print('Are you sure?')
    number = int(input('Enter the number of unused assets to confirm: '))
    if number != len(unused_assets):
        print('Canceled recycling.')
        return

    # Create a folder for all the files that will be sent to the recycle bin.
    # The folder's name will be the current datetime and this program's name.
    date_and_time = str(datetime.datetime.now()).replace(':', '').replace('.', '')
    new_folder_name = date_and_time + ' check_media'
    os.mkdir(new_folder_name)

    # Move all the files into the new folder.
    for asset_name in unused_assets.keys():
        new_path = os.path.join(new_folder_name, asset_name)
        os.rename(asset_name, new_path)
        # If the asset is an .html file, move the corresponding folder.
        if asset_name.endswith('.html'):
            asset_folder_name = asset_name[0:-5] + '_files'
            new_path = new_path[0:-5] + '_files'
            for retry in range(100):
                try:
                    os.rename(asset_folder_name, new_path)
                    break
                except OSError:
                    pass

    # Move the new folder to the recycle bin.
    send2trash(new_folder_name)
    print(f'\nAll unused assets sent to the recycle bin in the new folder {new_folder_name}\n')


if __name__ == '__main__':
    main()

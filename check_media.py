# This program searches the zettelkasten for missing assets, broken asset links, etc.
# (more details in the README).

# Internal
from common import *
from move_media import get_all_asset_links

# External
import os
import sys
import subprocess
import platform
from send2trash import send2trash
# import pyautogui


def check_media():
    try:
        # Get all the file names in the zettelkasten.
        zettel_paths, dir_asset_paths = get_file_paths()

        # Get all the file links in the zettels. This also finds all broken
        # asset links, and moves any assets in a downloads folder to the
        # default assets folder. asset_links is a Links object.
        asset_links = get_all_asset_links(zettel_paths)

        # Determine which assets are unlinked.
        unused_assets = find_unused_assets(dir_asset_paths, asset_links.names)  # Returns a dict of unused assets' paths and memory sizes.

        # Find zettels that are missing a 14-digit ID.
        zettels_without_ID = find_zettels_without_ID(zettel_paths)

        # Find zettels that are missing a title (a header level 1).
        zettels_without_title = find_zettels_without_title(zettel_paths)

        # Find zettels with no tags.
        untagged_zettels = find_untagged_zettels(zettel_paths)

        # Print info about what the program has done so far.
        print_summary(asset_links, unused_assets, zettels_without_ID, zettels_without_title, untagged_zettels)

        # Help the user decide what to do with each unused asset.
        manage_unused_assets(unused_assets)

    except SystemExit:
        pass


# For sorting a dictionary by value with the sorted() function.
def by_value(item):
    return item[1]


# Return a dict with keys of asset paths and values of asset file sizes.
def find_unused_assets(dir_asset_paths, linked_asset_names):
    # Find unused assets by comparing the zettelkasten's files and the file links in the zettels.
    unused_assets = dict()
    for dir_asset_path in dir_asset_paths:
        dir_asset_name = os.path.split(dir_asset_path)[-1]
        if dir_asset_name not in linked_asset_names:
            unused_assets[dir_asset_path] = os.path.getsize(dir_asset_path)
            # If the unused asset is an .html file, get the size of the corresponding folder too.
            if dir_asset_path.endswith('.html'):
                unused_assets[dir_asset_path] += get_size(dir_asset_path[0:-5] + '_files')

    # Sort the unused assets by descending value.
    sorted_unused_assets = dict()
    for key, value in sorted(unused_assets.items(), key=by_value, reverse=True):
        sorted_unused_assets[key] = value

    return sorted_unused_assets


# Find all zettels that are missing a 14-digit ID.
# Returns a list of file names.
def find_zettels_without_ID(zettel_paths):
    zettels_without_ID = []
    for zettel_path in zettel_paths:
        zettel_id = find_zettel_id(zettel_path)
        if not zettel_id.isnumeric():
            zettel_name = os.path.split(zettel_path)[-1]
            zettels_without_ID.append(zettel_name)

    return zettels_without_ID


# Find all zettels that do not have a header level 1.
# Returns a list of file names.
def find_zettels_without_title(zettel_paths):
    zettels_without_title = []
    for zettel_path in zettel_paths:
        title = get_zettel_title(zettel_path)
        if title == '':
            zettel_name = os.path.split(zettel_path)[-1]
            zettels_without_title.append(zettel_name)

    return zettels_without_title


# Return a list of all zettels with no tags.
def find_untagged_zettels(zettel_paths):
    untagged_zettels = []
    tag_pattern = re.compile(r'(?<=\s)#[a-zA-Z0-9_-]+')
    for zettel_path in zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        tag_match = tag_pattern.search(contents)
        if tag_match is None:
            untagged_zettels.append()

    return untagged_zettels


# Get the total memory size of an entire folder in bytes.
def get_size(start_path='.'):
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Skip the file if it is a symbolic link.
            if not os.path.islink(filepath):
                total_size += os.path.getsize(filepath)

    return total_size


# Print info about the broken links and unused assets.
# unused_assets is a dict of unused assets' paths and memory sizes.
def print_summary(asset_links, unused_assets, zettels_without_ID, zettels_without_title, untagged_zettels):
    print_broken_links(asset_links.broken)
    print_zettels_without_ID(zettels_without_ID)
    print_zettels_without_title(zettels_without_title)
    print_untagged_zettels(untagged_zettels)
    print_unused_assets(unused_assets)

    total_bytes = sum(unused_assets.values())

    print('\nSummary:')
    print(f' * Found {len(unused_assets)} unused asset(s) taking {format_bytes(total_bytes)} of memory.')
    print(f' * Found {len(asset_links.broken)} broken asset links.')
    print(f' * Found {len(zettels_without_ID)} zettels without a 14-digit ID.')
    print(f' * Found {len(zettels_without_title)} zettels without a title.')
    print(f' * Found {len(untagged_zettels)} zettels with no tags.')


def print_broken_links(links):
    if len(links):
        print('\nMissing assets:')
        for link in links:
            print(f'   {link}')


def print_zettels_without_ID(zettels_without_ID):
    if len(zettels_without_ID):
        print('\nZettels without a 14-digit ID:')
        for zettel_name in zettels_without_ID:
            print(f'   {zettel_name}')


def print_zettels_without_title(zettels_without_title):
    if len(zettels_without_title):
        print('\nZettels without a title:')
        for zettel_name in zettels_without_title:
            print(f'   {zettel_name}')


def print_untagged_zettels(untagged_zettels):
    if len(untagged_zettels) > 0:
        print('\nZettels without any tags:')
        for untagged_zettel in untagged_zettels:
            print(f'   {untagged_zettel}')


# Print the names and the bytes of each asset.
# unused_assets is a dict of unused assets' paths and memory sizes.
def print_unused_assets(unused_assets):
    if len(unused_assets) == 0:
        return

    # Get the length of the longest asset name.
    print('\nUnused assets:')
    unused_asset_paths = unused_assets.keys()
    unused_asset_names = []
    for path in unused_asset_paths:
        unused_asset_names.append(os.path.split(path)[-1])
    longest_asset_path = max(unused_asset_names, key=len)
    name_size = len(os.path.split(longest_asset_path)[-1])

    # Print the asset info in columns.
    for path, Bytes in unused_assets.items():
        name = os.path.split(path)[-1]
        Bytes = format_bytes(Bytes)
        print(f'   {name:<{name_size}}{Bytes:>11}')


# Help the user decide what to do with each unused asset.
def manage_unused_assets(unused_assets):
    # End the program if there are no unused assets to manage.
    if len(unused_assets) == 0:
        print()
        sys.exit(0)

    # Help the user decide what to do with each unused asset.
    print_menu()
    choice = input('> ')
    run_menu(choice, unused_assets)


def print_menu():
    print('\nMenu:')
    print('1. Choose what to do with each unused asset individually.')
    print('2. Send all unused assets to the recycle bin.')
    print('3. Exit')


# unused_assets is a dict of unused assets' paths and memory sizes.
def run_menu(choice, unused_assets):
    if choice == '1':
        validate_unused_assets(unused_assets)
    elif choice == '2':
        delete_all_unused_assets(unused_assets)
    else:
        print()
        sys.exit(0)


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
#   show the asset in file explorer / finder / etc.
#   ask the user whether to send it to the recycle bin.
# unused_assets is a dict of unused assets' paths and memory sizes.
def validate_unused_assets(unused_assets):
    print('\nChoose what to do with each unused asset.')
    print('You can enter q to quit.\n')
    for path, Bytes in unused_assets.items():
        # Print the asset name and memory.
        name = os.path.split(path)[-1]
        Bytes = format_bytes(Bytes)
        print(f'{name}{Bytes:>10}')

        # # Open the asset for the user to view.
        # os.startfile(path)
        # pyautogui.sleep(0.5)
        # asset_window = pyautogui.getActiveWindow()
        # # Bring the program's window back to the front.
        # pyautogui.hotkey('alt', 'tab')
        # choice = input('Send asset to the recycle bin? [y/n]: ')
        # # Close the asset window.
        # if path.endswith('.html'):
        #     pyautogui.hotkey('alt', 'tab')
        #     pyautogui.hotkey('ctrl', 'w')
        #     pyautogui.hotkey('alt', 'tab')
        # else:
        #     asset_window.close()

        # Show the asset in the explorer/finder/etc.
        if platform.system() == 'Windows':
            temp_path = path.replace('/', '\\')
            subprocess.Popen(['explorer', '/select,', temp_path])
        elif platform.system() == 'Darwin':  # This is the macOS.
            subprocess.call(['open', '-R', path])
        else:
            subprocess.call(['xdg-open', '-R', path])

        # Respond to the user's choice.
        if choice == 'y':
            delete_unused_asset(path)
            print('Asset sent to the recycle bin.\n')
        elif choice == 'n':
            print('Asset saved.\n')
        elif choice == 'q':
            sys.exit(0)
        else:
            print('Asset saved.\n')

    print('\nAll assets validated.\n')


# Send all unused assets to the recycle bin.
# unused_assets is a dict of unused assets' paths and memory sizes.
def delete_all_unused_assets(unused_assets):
    print('Are you sure?')
    number = int(input('Enter the number of unused assets to confirm: '))
    if number != len(unused_assets):
        print('Canceled recycling.')
        return
    for path in unused_assets.keys():
        delete_unused_asset(path)
    print(f'\nAll unused assets sent to the recycle bin.\n')


# Send one unused asset to the recycle bin.
# unused_asset is a dict of an unused asset's path and memory size.
def delete_unused_asset(path):
    send2trash(path)
    # If the asset is an .html file, move the corresponding folder.
    if path.endswith('.html'):
        folder_path = path[0:-5] + '_files'
        if os.path.isdir(folder_path):
            try:
                send2trash(folder_path)
            except OSError:
                print('OSError')
        else:
            print(f'Could not find folder \'{folder_path}\'.')


if __name__ == '__main__':
    check_media()

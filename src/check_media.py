# This program searches a zettelkasten for unused assets,
# broken file links, and various anti-patterns.

# Internal imports
try:
    from common import *
    from move_media import get_all_asset_links
except ModuleNotFoundError:
    from .common import *
    from .move_media import get_all_asset_links

# External imports
import os
import sys
from send2trash import send2trash


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

        # Try to repair any broken asset links by looking at unused assets with the same name.
        if len(asset_links.broken) > 0:
            repair_broken_asset_links(asset_links, unused_assets)

        # Help the user decide what to do with any unused assets.
        if len(unused_assets) > 0:
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
# Return a list of zettel links.
def find_zettels_without_ID(zettel_paths):
    zettels_without_ID = []
    for zettel_path in zettel_paths:
        zettel_id = find_zettel_id(zettel_path)
        if not zettel_id.isnumeric():
            zettel_link = get_zettel_link(zettel_path)
            zettels_without_ID.append(zettel_link)

    return zettels_without_ID


# Find all zettels that do not have a header level 1.
# Return a list of zettel links.
def find_zettels_without_title(zettel_paths):
    zettels_without_title = []
    for zettel_path in zettel_paths:
        title = get_zettel_title(zettel_path)
        if title == '':
            zettel_link = get_zettel_link(zettel_path)
            zettels_without_title.append(zettel_link)

    return zettels_without_title


# Find all zettels that don't have any tags.
# Return a list of zettel links.
def find_untagged_zettels(zettel_paths):
    untagged_zettels = []
    tag_pattern = re.compile(r'(?<=\s)#[a-zA-Z0-9_-]+')
    for zettel_path in zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        tag_match = tag_pattern.search(contents)
        if tag_match is None:
            zettel_link = get_zettel_link(zettel_path)
            untagged_zettels.append(zettel_link)

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
# asset_links is a Links object.
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
        for zettel_link in zettels_without_ID:
            print(f'   {zettel_link}')


def print_zettels_without_title(zettels_without_title):
    if len(zettels_without_title):
        print('\nZettels without a title:')
        for zettel_link in zettels_without_title:
            print(f'   {zettel_link}')


def print_untagged_zettels(untagged_zettels):
    if len(untagged_zettels) > 0:
        print('\nZettels without any tags:')
        for zettel_link in untagged_zettels:
            print(f'   {zettel_link}')


# Print the names and the bytes of each asset.
# unused_assets is a dict of unused assets' paths and memory sizes.
def print_unused_assets(unused_assets):
    if len(unused_assets) == 0:
        return

    # Get the length of the longest asset name.
    name_size = longest_name_len(unused_assets.keys())

    # Print the asset info in columns.
    print('\nUnused assets:')
    for path, Bytes in unused_assets.items():
        name = os.path.split(path)[-1]
        Bytes = format_bytes(Bytes)
        print(f'   {name:<{name_size}}{Bytes:>11}')


# Return the length of the longest file name in a list of file paths.
def longest_name_len(file_paths):
    file_names = []
    for path in file_paths:
        file_names.append(os.path.split(path)[-1])
    longest_asset_path = max(file_names, key=len)
    name_size = len(os.path.split(longest_asset_path)[-1])

    return name_size


# Try to repair any broken asset links by looking at unused assets with the same name.
# asset_links is a Links object.
# unused_assets is a dict of unused assets' paths and memory sizes.
def repair_broken_asset_links(asset_links, unused_assets):
    potential_matches = []  # A list of tuples: [(path_in_file, path_in_dir)]

    for path_in_file in asset_links.formatted:
        name_in_file = os.path.split(path_in_file)[-1]
        for path_in_dir in unused_assets.keys():
            name_in_dir = os.path.split(path_in_dir)[-1]

            if name_in_file == name_in_dir:
                potential_matches.append((path_in_file, path_in_dir))

    if len(potential_matches) > 0:
        # Ask the user if any of the potential matches are correct.
        print('\nPotential matches found between broken links and unused assets:')
        for match in potential_matches:
            print(f'   broken link:  \'{match[0]}\'')
            print(f'   unused asset: \'{match[1]}\'')
            print('       1. change link')
            print('       2. ignore')
            choice = input('>       ')
            if choice == '1':
                success = repair_broken_asset_link(match[0], match[1])
                if success:
                    # Update unused_assets.
                    del unused_assets[match[1]]


# Fix a broken asset link in the zettelkasten by changing zettel contents.
def repair_broken_asset_link(incorrect_link, correct_link):
    incorrect_pattern = rf'(?<=]\(){re.escape(incorrect_link)}(?=\))'
    all_zettel_paths = get_zettel_paths()

    for zettel_path in all_zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        contents, sub_count = re.subn(incorrect_pattern, correct_link, contents)
        if sub_count <= 0:
            print('       Error. Failed to fix broken link.')
            return False
        else:
            with open(zettel_path, 'w', encoding='utf8') as zettel:
                zettel.write(contents)
            print('       Link fixed.')
            return True


# Help the user decide what to do with each unused asset.
# unused_assets is a dict of unused assets' paths and memory sizes.
def manage_unused_assets(unused_assets):
    # Help the user decide what to do with each unused asset.
    print_unused_asset_menu()
    choice = input('> ')
    run_unused_asset_menu(choice, unused_assets)


def print_unused_asset_menu():
    print('\nMenu:')
    print('1. Choose what to do with each unused asset individually.')
    print('2. Send all unused assets to the recycle bin.')
    print('3. Exit')


# unused_assets is a dict of unused assets' paths and memory sizes.
def run_unused_asset_menu(choice, unused_assets):
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

        # Show the asset in explorer/finder/etc.
        show_file(path)

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
    number = input('Enter the number of unused assets to confirm: ')
    if number != str(len(unused_assets)):
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

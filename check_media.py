# Search the zettelkasten folder for unused assets,
# and let the user decide what to do with them.

# To add a new asset type to the program,
# change both the asset_types and asset_link_pattern variables.

import os
import sys
import re
# from PIL import Image
import send2trash
import datetime
import pyautogui


zettel_types = ('.md', '.markdown')
asset_types = ('.jpg', '.jpeg', '.png', '.pdf', '.mp4')
image_types = ('.jpg', '.jpeg', '.png')  # Not in use. Test the program and consider deleting.
asset_link_pattern = r'(?<=(\(|\\|/))([^(\(|\\|/)]+)\.(jpg|jpeg|png|pdf|mp4)\)'


def main():
    unused_assets, unused_bytes = find_unused_assets()
    print_unused_asset_info(unused_assets, unused_bytes)
    total_bytes = sum(unused_bytes)
    print(f'\nFound {len(unused_assets)} unused asset(s) taking {format_bytes(total_bytes)} of memory.')

    if len(unused_assets) == 0:
        return

    print('\nMenu:')
    print('1. Manually validate unused assets.')
    print('2. Send all unused assets to the recycle bin.')
    print('3. Exit')
    print('> ', end='', flush=True)
    choice = input()

    os.chdir('..')
    if choice == '1':
        validate_unused_assets(unused_assets)
    elif choice == '2':
        delete_unused_assets(unused_assets)
    else:
        sys.exit(0)


def find_unused_assets():
    zettel_names, asset_names = find_file_names()
    asset_links = find_asset_links(zettel_names)

    # Find unused assets by comparing the zettelkasten's files and the file links in the zettels.
    unused_assets_b = dict() # The keys are asset names, and the values are the asset file sizes.


    unused_assets = []
    unused_bytes = []
    for asset_name in asset_names:
        if asset_name not in asset_links:
            asset_path = '../' + asset_name
            unused_assets_b[asset_name] = os.path.getsize(asset_path)
            unused_assets.append(asset_name)
            unused_bytes.append(os.path.getsize(asset_path))

    return unused_assets, unused_bytes


def find_file_names():
    # Get all files in the current directory.
    file_names = os.listdir('..')

    # Of these files, we only want the zettels and the assets.
    zettel_names = []
    asset_names = []
    for file_name in file_names:
        if file_name.endswith(zettel_types):
            zettel_names.append(file_name)
        elif file_name.endswith(asset_types):
            asset_names.append(file_name)

    return zettel_names, asset_names


# Find the asset file links in the zettels.
def find_asset_links(zettel_names):
    asset_links = []

    # For each zettel.
    for zettel_name in zettel_names:
        zettel_path = '../' + zettel_name

        # Find all the links in the zettel.
        with open(zettel_path, 'r', encoding='utf8') as file:
            contents = file.read()
            new_links = re.findall(asset_link_pattern, contents)

            # Append this zettel's links to the list of all links.
            for new_link in new_links:
                asset_links.append(new_link[1] + '.' + new_link[2])

    return asset_links


# Print the names and the kilobytes of each unused asset.
def print_unused_asset_info(unused_assets, unused_bytes):
    if len(unused_assets) == 0:
        return
    name_size = len(max(unused_assets, key=len))  # The size of the longest asset name.
    print('\nUnused assets:')
    for i, _ in enumerate(unused_assets):
        Bytes = format_bytes(unused_bytes[i])
        print(f'{unused_assets[i]:<{name_size}}{Bytes:>12}')


# Convert bytes to kilobytes, megabytes, etc.
# Returns a string of the converted bytes and the appropriate units.
def format_bytes(Bytes):
    power = 0
    while Bytes > 1024:
        power += 3
        Bytes /= 1024
    result = str(round(Bytes, 2))
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


# For each asset:
#   open the asset
#   ask the user what to do with it
def validate_unused_assets(unused_assets):
    print('\nChoose what to do with each unused asset.')
    print('\nYou can enter q to quit.\n')
    for asset_name in unused_assets:
        print(asset_name)

        os.startfile(asset_name)  # Open the asset for the user to view.
        pyautogui.sleep(0.5)
        asset_window = pyautogui.getActiveWindow()
        pyautogui.hotkey('alt', 'tab')  # Bring the program's window back to the front.
        choice = input('Send asset to the recycle bin? [y/n]: ')
        asset_window.close()

        '''
            # If the code above doesn't work for certain filetypes, use this:
            # https://helloacm.com/execute-external-programs-the-python-ways/
            if asset_name.endswith(image_types):
                with Image.open(asset_path) as image:
                    image.show()
                    choice = input('Send asset to the recycle bin? [y/n]: ')
            elif asset_name.endswith('.pdf'):
                pdf = Popen(asset_path, shell=True)
                choice = input('Send asset to the recycle bin? [y/n]: ')
                pdf.kill() # Close the pdf.
            elif asset_name.endswith('.mp4'):
                # TODO.
            else:
                print('Error: file type not yet supported.')
                choice = 'n'
        '''

        # Respond to the user's choice.
        if choice == 'y':
            send2trash.send2trash(asset_name)
            print('Asset sent to the recycle bin.')
        elif choice == 'n':
            print('Asset saved.')
        elif choice == 'q':
            sys.exit(0)
        else:
            print('Asset saved.')

    print('\nAll assets validated.')


# Send all unused assets to the recycle bin in a new folder.
def delete_unused_assets(unused_assets):
    print('Are you sure?')
    number = int(input('Enter the number of unused assets to confirm: '))
    if number != len(unused_assets):
        print('Canceled recycling.')
        return

    # Create a folder for all the files that will be sent to the recycle bin.
    # The folder's name will be the current datetime and this program's name.
    date_and_time = str(datetime.datetime.now())
    new_folder_name = date_and_time + ' check_media'
    new_folder_path = '../' + new_folder_name
    os.mkdir(new_folder_path)

    # Move all the files into the new folder.
    for asset_name in unused_assets:
        asset_path = '../' + asset_name
        new_path = os.path.join(new_folder_path, asset_name)
        os.rename(asset_path, new_path)

    # Move the new folder to the recycle bin.
    send2trash.send2trash(new_folder_path)
    print(f'\nAll unused assets sent to the recycle bin in the new folder {new_folder_name}\n')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass

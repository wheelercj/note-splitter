# This program splits one or more zettels each into multiple zettels.
# The split happens based on a header level of your choice, and the copied contents
# are replaced with links to the new zettels. Each new zettel has a backlink.
# Before running this program, put the '#split' tag in each zettel you want to split
# so the program knows which zettels to split. In the original zettel, any tags
# above the chosen header level to split by will be copied into each of the new
# zettels (except '#split'). The new zettels will be created in the same folder
# as their respective source zettel.

# Internal
from common import get_zettel_paths, get_zettel_titles, get_zettel_title

# External
import os
import re
import datetime
from tkinter import Tk, messagebox
from tkinter.simpledialog import askinteger


def split_zettel_main():
    # Find the file paths of all zettels that contain the '#split' tag.
    zettels_to_split = get_zettels_to_split()
    # Display the titles of the zettels found, and ask for the header level to split by.
    header_level = get_header_level(zettels_to_split)
    # Split the zettels.
    split_zettels(zettels_to_split, header_level)


# Find the file paths of all zettels that contain the '#split' tag.
def get_zettels_to_split():
    zettels_to_split = []
    pattern = re.compile(r'#split')
    zettel_paths = get_zettel_paths()

    for zettel_path in zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        match = pattern.search(contents)
        if match is not None:
            zettels_to_split.append(zettel_path)

    return zettels_to_split


# Display the titles of the zettels found, and ask for the header level to split by.
def get_header_level(zettels_to_split):
    Tk().withdraw()
    zettel_titles = get_zettel_titles(zettels_to_split)

    # Change the list of zettel titles into an easily readable string.
    instructions = 'Zettels found containing \'#split\':\n'
    for title in zettel_titles:
        instructions = instructions + ' * ' + title + '\n'
    instructions = instructions + '\nEnter the header level to split by.'

    invalid_input = True
    while invalid_input:
        header_level = askinteger('Split zettel', instructions)
        if header_level < 1 or header_level > 6:
            messagebox.showinfo(title='Split zettel', message='Header level must be within 1-6.')
        else:
            invalid_input = False

    return header_level


class HeaderNotFoundError(ValueError):
    pass


# Split the zettels by the chosen header level.
def split_zettels(zettels_to_split, header_level):
    tag_pattern = re.compile(r'(?<=\s)#[a-zA-Z0-9_-]+')
    chosen_header_pattern = re.compile(rf'^#{{{header_level}}} .+', re.MULTILINE)
    header_pattern = re.compile(r'(^#{1,6} .+)', re.MULTILINE)
    new_zettel_id = generate_zettel_id()
    new_zettel_titles = []

    for source_zettel_path in zettels_to_split:
        with open(source_zettel_path, 'r', encoding='utf8') as zettel:
            source_zettel_contents = zettel.read()

        try:
            # Find all the tags above the first of the chosen header level.
            global_tags = find_global_tags(source_zettel_contents, chosen_header_pattern, tag_pattern)

            # Find the first header of level header_level.
            header_match1 = chosen_header_pattern.search(source_zettel_contents)
            # TODO: ignore the contents of code blocks during all searches for headers throughout this entire program.

            need_new_match1 = False
            at_end_of_file = False
            while not at_end_of_file:  # Each iteration of this loop creates one new zettel.
                # If the previous header search found a header of a level larger than header_level.
                if need_new_match1:
                    need_new_match1 = False
                    header_match1 = chosen_header_pattern.search(source_zettel_contents, header_match2.end())
                    if header_match1 is None:
                        at_end_of_file = True
                        break

                # Find the next header of any level.
                header_match2 = header_pattern.search(source_zettel_contents, header_match1.end())

                # If the search reached the end of the contents without finding a match.
                if header_match2 is None:
                    at_end_of_file = True

                    start = header_match1.start()
                    end = len(source_zettel_contents)
                    split_section(source_zettel_contents, start, end, header_pattern, new_zettel_id, source_zettel_path, global_tags, header_level, new_zettel_titles)

                # If the header is of a smaller level (more hashes) than header_level.
                elif header_match2[0].count('#') > header_level:  # TODO: as this is now, it will not work correctly if the header contains hashes after the hashes that make it a header.
                    # Ignore the match and find the next one.
                    continue

                # If the header is of level header_level or a larger level (fewer hashes).
                else:
                    # If the header is of a larger level (fewer hashes) than header_level.
                    if header_match2[0].count('#') < header_level:  # TODO: as this is now, it will not work correctly if the header contains hashes after the hashes that make it a header.
                        # A new match1 will be needed in the next loop iteration.
                        need_new_match1 = True

                    start = header_match1.start()
                    end = header_match2.start()
                    split_section(source_zettel_contents, start, end, header_pattern, new_zettel_id, source_zettel_path, global_tags, header_level, new_zettel_titles)

                new_zettel_id = str(int(new_zettel_id) + 1)
                header_match1 = header_match2

        except HeaderNotFoundError:
            zettel_title = get_zettel_title(source_zettel_path)
            print(f'   Could not find a header of level {header_level} in \'{zettel_title}\'')

    # Print a summary of what the program did.
    message = 'New zettels created:'
    for new_zettel_title in new_zettel_titles:
        message = message + '\n * ' + new_zettel_title
    messagebox.showinfo(title='Split zettel', message=message)


# Generate a 14-digit zettel ID that represents the current date and time.
# The format is YYYYMMDDhhmmss.
def generate_zettel_id():
    zettel_id = str(datetime.datetime.now())
    zettel_id = zettel_id[:19]  # Remove the microseconds.
    zettel_id = zettel_id.replace('-', '').replace(':', '').replace(' ', '')
    return zettel_id


# Find all the tags above the first of the chosen header level in one zettel's contents.
def find_global_tags(source_zettel_contents, chosen_header_pattern, tag_pattern):
    header_match = chosen_header_pattern.search(source_zettel_contents)
    if header_match is None:
        raise HeaderNotFoundError()

    global_part_end = header_match.start()
    global_part = source_zettel_contents[:global_part_end]  # The part of the file above the chosen header level.
    global_tags = tag_pattern.findall(global_part)
    if '#split' in global_tags:
        global_tags.remove('#split')

    return global_tags


# Get the zettelkasten-style link to a zettel, in the format:
# '[[20201215093128]] This is the zettel title'
def get_zettel_link(zettel_path):
    zettel_id = find_zettel_id(zettel_path)
    if zettel_id == -1:
        raise ValueError('Zettel ID not found.')

    zettel_title = get_zettel_title(zettel_path)
    zettel_link = '[[' + zettel_id + ']] ' + zettel_title

    return zettel_link


# Find the 14-digit ID of a zettel (the format is YYYYMMDDhhmmss).
# The zettel ID can be in the file name or in the file's contents.
def find_zettel_id(zettel_path):
    zettel_id_pattern = re.compile(r'(?<!\[\[)\d{14}(?!]])')

    # Search for the zettel ID in the file's name.
    zettel_name = os.path.split(zettel_path)[1]
    zettel_id_match = zettel_id_pattern.search(zettel_name)
    if zettel_id_match is None:
        # Search for the zettel ID in the zettel's contents.
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        zettel_id_match = zettel_id_pattern.search(contents)
        if zettel_id_match is None:
            # This zettel has no ID.
            return -1

    return zettel_id_match[0]


# Split off one section of a zettel into a new zettel.
def split_section(source_zettel_contents, start, end, header_pattern, new_zettel_id, source_zettel_path, global_tags, header_level, new_zettel_titles):
    new_zettel_contents = source_zettel_contents[start:end]

    # Get the new zettel's title.
    end_of_title = new_zettel_contents.find('\n')
    new_zettel_title = new_zettel_contents[:end_of_title]
    new_zettel_title = new_zettel_title.replace('#', '')
    # Remove any spaces on either side of the string.
    new_zettel_title = new_zettel_title.strip()
    new_zettel_titles.append(new_zettel_title)

    # Remove the copied contents from the source zettel, and insert a link to the new zettel.
    source_zettel_contents = source_zettel_contents[:start] + '\n[[' + new_zettel_id + ']] ' + new_zettel_title + '\n' + source_zettel_contents[end:]

    # Change the header levels in the new zettel contents.
    header_level_difference = header_level - 1
    if header_level_difference > 0:
        # Mark each header that needs to change with a character that's not likely to already be in the file.
        new_zettel_contents = header_pattern.sub(r'␝\1', new_zettel_contents)
        # Delete each instance of the ␝ character and some following hashes.
        landmark_pattern = re.compile('␝' + '#' * header_level_difference)
        new_zettel_contents = landmark_pattern.sub('', new_zettel_contents)

    # Insert the global tags into the new zettel under the title.
    global_tag_str = ''
    for tag in global_tags:
        global_tag_str = global_tag_str + tag + ' '
    new_zettel_contents = new_zettel_contents[:end_of_title] + '\n' + global_tag_str + new_zettel_contents[end_of_title:]

    # Insert a backlink to the source zettel in the new zettel.
    try:
        backlink = get_zettel_link(source_zettel_path)
        new_zettel_contents = new_zettel_contents + '\n## see also:\n* topic outline: ' + backlink
    except ValueError as e:
        if e == 'Zettel ID not found.':
            zettel_title = get_zettel_title(source_zettel_path)
            print(f'   Could not create a backlink to \'{zettel_title}\' because it has no zettel ID.')
        else:
            raise

    # Create a new zettel using new_zettel_id, in the same folder as the source zettel.
    new_zettel_name = new_zettel_id + '.md'
    folder_path = os.path.split(source_zettel_path)[0]
    new_zettel_path = os.path.join(folder_path, new_zettel_name)

    # Save both zettels.
    print('Ready to save the source zettel and a new zettel, but not doing that because the program hasn\'t been tested enough yet.')
    # with open(new_zettel_path, 'w', encoding='utf8') as zettel:
    #     zettel.write(new_zettel_contents)
    # with open(source_zettel_path, 'w', encoding='utf8') as zettel:
    #     zettel.write(source_zettel_contents)


if __name__ == '__main__':
    split_zettel_main()

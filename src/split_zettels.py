# This program splits one or more zettels each into multiple zettels.
# The split happens based on a header level of your choice, and the copied contents
# are replaced with links to the new zettels.
# Before running this program, put the '#split' tag in each zettel you want to split
# so the program knows which zettels to split. In the original zettel, any tags
# above the chosen header level to split by will be copied into each of the new
# zettels (except '#split'). The new zettels will be created in the same folder
# as their respective source zettel.

# Internal imports
try:
    from common import *
    from zettels import Zettels
except ModuleNotFoundError:
    from .common import *
    from .zettels import Zettels

# External imports
import os
import re
import sys
from tkinter import Tk, messagebox
from tkinter.simpledialog import askinteger


def split_zettel_main():
    # Find the file paths of all zettels that contain the '#split' tag.
    z_to_split = get_zettels_to_split()
    # Display the titles of the zettels found, and ask for the header level to split by.
    header_level = get_header_level(z_to_split)
    # Split each chosen zettel into multiple zettels.
    new_zettels, zettels_sans_h = split_zettels(z_to_split, header_level)

    print_summary(new_zettels, zettels_sans_h.links)


# Find the file paths of all zettels that contain the '#split' tag.
def get_zettels_to_split():
    z_to_split = []
    pattern = re.compile(r'#split')
    zettel_paths = get_zettel_paths()

    for zettel_path in zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        match = pattern.search(contents)
        if match is not None:
            z_to_split.append(zettel_path)

    return z_to_split


# Display the titles of the zettels found, and ask for the header level to split by.
def get_header_level(z_to_split):
    Tk().withdraw()
    zettel_links = get_zettel_links(z_to_split)

    # Change the list of zettel links into an easily readable string.
    instructions = 'Zettels found containing \'#split\':\n'
    for z_link in zettel_links:
        instructions = instructions + ' * ' + z_link + '\n'
    instructions = instructions + '\nEnter the header level to split by.'

    invalid_input = True
    while invalid_input:
        header_level = askinteger('Split zettel', instructions)
        if header_level is None:
            sys.exit(0)

        if header_level < 1 or header_level > 6:
            messagebox.showinfo(title='Split zettel', message='Header level must be within 1-6.')
        else:
            invalid_input = False

    return header_level


class HeaderNotFoundError(ValueError):
    pass


# Split one or more zettels each into multiple zettels by the chosen header level.
def split_zettels(z_to_split, header_level):
    new_zettels = Zettels()
    zettels_sans_h = Zettels()
    new_z_id = generate_zettel_id()

    for source_z_path in z_to_split:
        try:
            split_zettel(source_z_path, header_level, new_z_id, new_zettels)
            remove_split_tag(source_z_path)
        except HeaderNotFoundError:
            z_link = get_zettel_link(source_z_path)
            zettels_sans_h.append(link=z_link, path=source_z_path)

    return new_zettels, zettels_sans_h


# Split one zettel into multiple zettels by the chosen header level.
def split_zettel(source_z_path, header_level, new_z_id, new_zettels):
    with open(source_z_path, 'r', encoding='utf8') as zettel:
        source_z_contents = zettel.read()

    tag_pattern = re.compile(r'(?<=\s)#[a-zA-Z0-9_-]+')
    chosen_header_pattern = re.compile(rf'^#{{{header_level}}} .+')  # Use re.MULTILINE with this pattern.
    header_pattern = re.compile(r'(^#{1,6} .+)')  # Use re.MULTILINE with this pattern.

    # Find all the tags above the first of the chosen header level.
    global_tags = find_global_tags(source_z_contents, chosen_header_pattern, tag_pattern)

    # Find the first header of level header_level.
    header_match1 = chosen_header_pattern.search(source_z_contents, re.MULTILINE)
    # TODO: ignore the contents of code blocks during all searches for headers throughout this entire program.

    need_new_match1 = False
    at_end_of_file = False
    while not at_end_of_file:  # Each iteration of this loop creates one new zettel.
        # If the previous header search found a header of a level larger (fewer hashes) than header_level.
        if need_new_match1:
            need_new_match1 = False
            header_match1 = chosen_header_pattern.search(source_z_contents, header_match2.end(), re.MULTILINE)
            if header_match1 is None:
                at_end_of_file = True

        if not at_end_of_file:
            # Find the next header of any level.
            header_match2 = header_pattern.search(source_z_contents, header_match1.end(), re.MULTILINE)

            # If the search reached the end of the contents without finding a match.
            if header_match2 is None:
                at_end_of_file = True

                section_start = header_match1.start()
                section_end = len(source_z_contents)
                source_z_contents = split_section(source_z_contents, section_start, section_end, source_z_path, header_level, header_pattern, global_tags, new_z_id, new_zettels)

            else:
                header_match2_count = header_match2[0].split(' ')[0].count('#')
                # If the header is of level header_level or a larger level (fewer hashes).
                if header_match2_count <= header_level:
                    # If the header is of a larger level (fewer hashes) than header_level.
                    if header_match2_count < header_level:
                        # A new header_match1 will be needed in the next loop iteration.
                        need_new_match1 = True

                    section_start = header_match1.start()
                    section_end = header_match2.start()
                    source_z_contents = split_section(source_z_contents, section_start, section_end, source_z_path, header_level, header_pattern, global_tags, new_z_id, new_zettels)

                new_z_id = str(int(new_z_id) + 1)
                header_match1 = header_match2


# Find all the tags above the first of the chosen header level in one zettel's contents.
def find_global_tags(source_z_contents, chosen_header_pattern, tag_pattern):
    header_match = chosen_header_pattern.search(source_z_contents, re.MULTILINE)
    if header_match is None:
        raise HeaderNotFoundError()

    global_section_end = header_match.start()
    global_section = source_z_contents[:global_section_end]  # The part of the file above the chosen header level.
    global_tags = tag_pattern.findall(global_section)
    if '#split' in global_tags:
        global_tags.remove('#split')

    return global_tags


# Split off one section of the source zettel into a new zettel.
def split_section(source_z_contents, section_start, section_end, source_z_path, header_level, header_pattern, global_tags, new_z_id, new_zettels):
    new_z_contents = source_z_contents[section_start:section_end]
    new_z_contents = normalize_headers(new_z_contents, header_level, header_pattern)
    new_z_title, title_end_pos = get_section_title(new_z_contents, new_z_titles)
    new_z_contents = insert_tags(global_tags, new_z_contents, title_end_pos)
    new_z_contents = insert_backlink(new_z_contents, source_z_path)
    new_z_path, new_z_name = create_new_zettel(new_z_id, source_z_path)
    new_zettels.append(new_z_path, new_z_name, new_z_id, new_z_title, new_z_link)

    # Remove the copied contents from the source zettel, and insert a link to the new zettel.
    source_z_contents = source_z_contents[:section_start] + '\n[[' + new_z_id + ']] ' + new_z_title + '\n' + source_z_contents[section_end:]

    print('Ready to save the source zettel and a new zettel, but not doing that because the program hasn\'t been tested enough yet.')
    # save_zettels(new_z_path, new_z_contents, source_z_path, source_z_contents)

    return source_z_contents


# Change the top header to have 1 hash, and change all the
# other headers by the same amount (all the other headers will
# have more hashes since this program splits by level header_level).
def normalize_headers(section_contents, header_level, header_pattern):
    header_level_difference = header_level - 1
    if header_level_difference > 0:
        # Mark each header with a character that's not likely to already be in the contents.
        section_contents = header_pattern.sub(r'␝\1', section_contents, re.MULTILINE)
        # Delete each instance of the ␝ character and some following hashes.
        landmark_pattern = re.compile('␝' + '#' * header_level_difference)
        section_contents = landmark_pattern.sub('', section_contents)

    return section_contents


# Get the title of the first header in a zettel section.
def get_section_title(section_contents, new_zettel_titles):
    title_end_pos = section_contents.find('\n')
    new_zettel_title = section_contents[:title_end_pos]
    new_zettel_title = new_zettel_title.replace('#', '')
    # Remove any spaces on either side of the string.
    new_zettel_title = new_zettel_title.strip()
    new_zettel_titles.append(new_zettel_title)

    return new_zettel_title, title_end_pos


# Insert tags under the title of a zettel.
def insert_tags(tags, zettel_contents, title_end_pos):
    global_tag_str = ''
    for tag in tags:
        global_tag_str = global_tag_str + tag + ' '
    zettel_contents = zettel_contents[:title_end_pos] + '\n' + global_tag_str + zettel_contents[title_end_pos:]
    return zettel_contents


# Insert a backlink to the source zettel in the new zettel.
def insert_backlink(new_z_contents, source_z_path):
    backlink = get_zettel_link(source_z_path)
    new_z_contents = new_z_contents + '\n\n## see also:\n* topic outline: ' + backlink
    return new_z_contents


# Create a new zettel in the same folder as the source zettel.
def create_new_zettel(new_z_id, source_z_path):
    new_z_name = new_z_id + '.md'
    folder_path = os.path.split(source_z_path)[0]
    new_z_path = os.path.join(folder_path, new_z_name)
    return new_z_path, new_z_name


def save_zettels(new_z_path, new_z_contents, source_z_path, source_z_contents):
    with open(new_z_path, 'x', encoding='utf8') as zettel:
        zettel.write(new_z_contents)
    with open(source_z_path, 'w', encoding='utf8') as zettel:
        zettel.write(source_z_contents)


# Print a summary of what the program did.
def print_summary(new_zettels, z_without_h_links):
    message = ''
    if len(new_zettels):
        message += 'New zettels created:'
        for new_z_link in new_zettels.links:
            message += '\n * ' + new_z_link
    if len(z_without_h_links):
        message += '\nCould not find the chosen header level in zettels:'
        for z_link in z_without_h_links:
            message += '\n' + z_link

    messagebox.showinfo(title='Split zettel', message=message)


# Remove all instances of the tag '#split' from a zettel.
def remove_split_tag(zettel_path):
    with open(zettel_path, 'r', encoding='utf8') as zettel:
        contents = zettel.read()
    contents = re.sub(r'#split', '', contents)
    with open(zettel_path, 'w', encoding='utf8') as zettel:
        zettel.write(contents)


if __name__ == '__main__':
    split_zettel_main()

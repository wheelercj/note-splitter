# Convert zettelkasten-style links to
# markdown-style links, or vice versa.

# External
import re
import sys


def convert_links():
    # Get the list of names of zettels to convert links in.
    zettel_paths = get_target_zettel_paths('../.gitignore')
    print(f'Found {len(zettel_paths)} zettels:')
    print(zettel_paths)

    if len(zettel_paths) == 0:
        sys.exit(0)

    try:
        while True:
            print('\nConvert links:')
            print('1. from zettelkasten to markdown style')
            print('2. from markdown to zettelkasten style')
            print('3. quit')
            choice = int(input('> '))

            if choice == 1:
                convert(r'\[\[(\d{14})\]\]', r'[§](\1.md)', zettel_paths)
            elif choice == 2:
                convert(r'\[§\]\((\d{14})\.md\)', r'[[\1]]', zettel_paths)
            else:
                sys.exit(0)

    except SystemExit:
        pass


# Parameter: the path to the file that contains the names of zettels to convert links in.
# Returns the list of names of those zettels.
# The zettel names must be the 14 digits of the file ID, followed by `.md`.
def get_target_zettel_paths(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
    except OSError:
        print(f'File not found: {file_path}')
        sys.exit(0)
    matches = re.findall(r'(\d{14}\.md)', contents)
    return matches


# Parameters:
# old_link_pattern is the regex pattern of the current links.
# new_link_name is the string that all the links will be changed to,
#   which can contain references to groups in old_link_pattern.
# zettel_paths is a list of paths to all the zettels to convert links in.
def convert(old_link_pattern, new_link_name, zettel_paths):
    zettel_count = len(zettel_paths)
    total_char_count = 0
    total_n_replaced = 0

    for zettel_path in zettel_paths:
        try:
            with open(zettel_path, 'r') as zettel:
                contents = zettel.read()
            char_count_1 = len(contents)

            # Use regex to find the links, and then convert them.
            new_contents, n_replaced = re.subn(old_link_pattern, new_link_name, contents)
            char_count_2 = len(new_contents)

            # Save contents back to the zettel.
            if n_replaced > 0:
                with open(zettel_path, 'w') as zettel:
                    zettel.write(new_contents)

            # Print character change stats.
            char_count = char_count_2 - char_count_1
            print(f'Changed {zettel.name} by {char_count} characters with {n_replaced} links converted.')
            total_char_count += char_count
            total_n_replaced += n_replaced

        except OSError:
            print(f'Zettel not found: {zettel_path}')

    print(f'\nChanged {zettel_count} zettels by a total of', end='', flush=True)
    print(f' {total_char_count} characters with {total_n_replaced} links converted.')


if __name__ == '__main__':
    convert_links()

# Convert zettelkasten-style links to
# markdown-style links, or vice versa.

# External
import re
import sys
import os


def main():
    # Get the list of names of files to convert links in.
    os.chdir('..')
    file_names = get_target_file_names('.gitignore')
    print(f'Found {len(file_names)} file names:')
    print(file_names)

    if len(file_names) == 0:
        sys.exit(0)

    try:
        while True:
            print('\nConvert links:')
            print('1. from zettelkasten to markdown style')
            print('2. from markdown to zettelkasten style')
            print('3. quit')
            choice = int(input('> '))

            if choice == 1:
                convert_links(r'\[\[(\d{14})\]\]', r'[§](\1.md)', file_names)
            elif choice == 2:
                convert_links(r'\[§\]\((\d{14})\.md\)', r'[[\1]]', file_names)
            else:
                sys.exit(0)

    except SystemExit:
        pass


# Parameter: the file that contains the names of files to convert links in.
# Returns the list of names of those files.
# The zettel names must be the 14 digits of the file ID, followed by `.md`.
def get_target_file_names(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
    except OSError:
        print(f'File not found: {file_name}')
        sys.exit(0)
    matches = re.findall(r'(\d{14}\.md)', contents)
    return matches


# Parameters:
# old_link_pattern is the regex pattern of the current links.
# new_link_name is the string that all the links will be changed to,
#   which can contain references to groups in old_link_pattern.
def convert_links(old_link_pattern, new_link_name, file_names):
    file_count = len(file_names)
    total_char_count = 0
    total_n_replaced = 0

    for file_name in file_names:
        try:
            with open(file_name, 'r') as file:
                contents = file.read()
            char_count_1 = len(contents)

            # Use regex to find the links, and then convert them.
            new_contents, n_replaced = re.subn(old_link_pattern, new_link_name, contents)
            char_count_2 = len(new_contents)

            # Save contents back to the file.
            if n_replaced > 0:
                with open(file_name, 'w') as file:
                    file.write(new_contents)

            # Print character change stats.
            char_count = char_count_2 - char_count_1
            print(f'Changed {file.name} by {char_count} characters with {n_replaced} links converted.')
            total_char_count += char_count
            total_n_replaced += n_replaced

        except OSError:
            print(f'File not found: {file_name}')

    print(f'\nChanged {file_count} files by a total of', end='', flush=True)
    print(f' {total_char_count} characters with {total_n_replaced} links converted.')


if __name__ == '__main__':
    main()

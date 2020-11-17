# Replaces a given regex pattern with a given string
# throughout the entire zettelkasten.

# Internal
from common import get_zettel_names

# External
import re
import sys


def main():
    try:
        zettel_names = get_zettel_names()

        print('Find and replace a regex pattern with a')
        print('string throughout the entire zettelkasten.')

        find_pattern = input('\nFind pattern: ')
        try:
            compiled_pattern = re.compile(find_pattern)
        except re.error as e:
            print(e)
            sys.exit(0)
        print(f'\nFinding pattern \'{find_pattern}\'')
        total_matches = print_matches(compiled_pattern, zettel_names)

        if total_matches == 0:
            sys.exit(0)

        replacement_string = input('Replace with string: ')
        print(f'Ready to replace pattern \'{find_pattern}\' with string \'{replacement_string}\'')
        print('Are you sure?')
        number = int(input('Enter the number of pattern matches to confirm: '))
        if number != total_matches:
            print('\nCanceled replacement.')
        else:
            print(f'\nReplacing pattern \'{find_pattern}\' with string \'{replacement_string}\'')
            total_replaced = replace_pattern(compiled_pattern, replacement_string, zettel_names)
            print(f'Replaced all {total_replaced} matches.')
            if total_replaced != total_matches:
                print('Why was the total replaced different from the total matches?')

    except SystemError:
        pass


# Returns the total number of matches.
def print_matches(compiled_pattern, zettel_names):
    total_matches = 0
    for zettel_name in zettel_names:
        zettel_path = '../' + zettel_name
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        matches = compiled_pattern.findall(contents)
        total_matches += len(matches)

        if len(matches) > 0:
            print(f'Matches in {zettel_name}:')
        for match in matches:
            print(f'    {match}')

    print(f'\nFound {total_matches} matches.\n')
    return total_matches


# Returns the total number of replacements.
def replace_pattern(compiled_pattern, replacement_string, zettel_names):
    total_replaced = 0
    for zettel_name in zettel_names:
        zettel_path = '../' + zettel_name
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        new_contents, n_replaced = compiled_pattern.subn(replacement_string, contents)
        total_replaced += n_replaced
        if n_replaced > 0:
            with open(zettel_path, 'w', encoding='utf8') as zettel:
                zettel.write(new_contents)

    return total_replaced


if __name__ == '__main__':
    main()

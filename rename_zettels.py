# Rename all zettels that have more than just their 14-digit
# ID in their name to just the 14-digit ID.

# Internal
from common import zettelkasten_path, get_zettel_names

# External
import os
import re
import sys


def rename_zettels():
    os.chdir(zettelkasten_path)
    zettel_names = get_zettel_names(os.listdir())

    # Get a list of all zettel names that have more than just their ID.
    long_names = []
    for zettel_name in zettel_names:
        if len(zettel_name) > 17 and re.match(r'\d{14}', zettel_name) and zettel_name.endswith('.md'):
            long_names.append(zettel_name)

    # Print the names of all zettels with long names.
    print('\nZettels with long names:')
    for name in long_names:
        print(f'   {name}')

    print(f'\nFound {len(long_names)} zettels with more than just their 14-digit ID in their names.')

    if (long_names == 0):
        print()
        sys.exit(0)

    print('\nWould you like to rename all the zettels to only their 14-digit ID?')
    number = int(input('Enter the number of zettels with long names to continue: '))

    if (number != len(long_names)):
        print('\nCanceled renaming.')
        sys.exit(0)

    else:  # Rename the zettels.
        for long_name in long_names:
            name, ext = os.path.splitext(long_name)
            new_name = name[:14] + ext
            os.rename(long_name, new_name)

        print(f'\nRenamed {len(long_names)} zettels.')


if __name__ == "__main__":
    rename_zettels()

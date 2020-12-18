# Rename all zettels that have more than just their 14-digit
# ID in their name to just the 14-digit ID.

# Internal
if __package__ is None:
    from common import get_zettel_paths
else:
    from .common import get_zettel_paths

# External
import os
import re
import sys


def rename_zettels():
    zettel_paths = get_zettel_paths()

    # Get a list of all zettel names that have more than just their ID.
    long_paths = []
    for zettel_path in zettel_paths:
        zettel_name = os.path.split(zettel_path)[1]
        if len(zettel_name) > 17 and re.match(r'\d{14}', zettel_name) and zettel_name.endswith('.md'):
            long_paths.append(zettel_path)

    # Print the names of all zettels with long names.
    print('\nZettels with long names:')
    for path in long_paths:
        name = os.path.split(path)[1]
        print(f'   {name}')

    print(f'\nFound {len(long_paths)} zettels with more than just their 14-digit ID in their names.')

    if (long_paths == 0):
        print()
        sys.exit(0)

    print('\nWould you like to rename all the zettels to only their 14-digit ID?')
    number = int(input('Enter the number of zettels with long names to continue: '))

    if (number != len(long_paths)):
        print('\nCanceled renaming.')
        sys.exit(0)

    else:  # Rename the zettels.
        for long_path in long_paths:
            path, name = os.path.split(long_path)
            name, ext = os.path.splitext(name)
            new_path = os.path.join(path, name[:14] + ext)
            os.rename(long_path, new_path)

        print(f'\nRenamed {len(long_paths)} zettels.')


if __name__ == "__main__":
    rename_zettels()

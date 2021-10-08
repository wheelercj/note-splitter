# external imports
from typing import List

# internal imports
from note import Note, get_chosen_notes


def main():
    notes: List[Note] = get_chosen_notes()


if __name__ == '__main__':
    main()

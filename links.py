# This class is for storing file paths that are asset links.

import os


class Links:
    def __init__(self):
        self.originals = []  # The file paths as they appear in the zettel.
        self.formatted = []  # The file paths in a modified form that is easier for the program to use.
        self.names = []     # The names of the files (the last part of the file paths).
        self.broken = []    # The original file paths whose files no longer exist or were moved.

    def append(self, file_path, file_name):
        original = file_path
        self.originals.append(original)
        self.names.append(file_name)
        self.__format(file_path)

        # Determine whether the link is broken.
        if not os.path.exists(self.formatted[-1]):
            self.broken.append(original)

    # Change the form of an asset link to make it easier to use.
    def __format(self, file_path):
        # Remove 'file://' from the beginning of any file links that have it.
        if file_path.startswith('file://'):
            file_path = file_path[7:]
        # Make any relative file links absolute.
        file_path = os.path.abspath(file_path)
        # Replace all instances of '\' with '/'.
        file_path = file_path.replace('\\', '/')

        self.formatted.append(file_path)

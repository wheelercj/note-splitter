# This class is for storing file paths that are asset links.

# Internal
from settings import settings

# External
import os


class Links:
    def __init__(self):
        # These lists are parallel, except for self.broken.
        self.originals = []  # The file paths as they appear in the zettel.
        self.formatted = []  # The file paths in a modified form that is easier for the program to use.
        self.names = []      # The names of the files (the last part of the file paths).
        self.broken = []     # The original file paths whose files no longer exist or were moved.

    def append(self, file_path, file_name):
        original = file_path
        self.originals.append(original)
        self.names.append(file_name)
        self.formatted.append(format_link(file_path))
        # Determine whether the link is broken.
        if not os.path.exists(self.formatted[-1]):
            self.broken.append(original)

    def add(self, links_object):
        for i, _ in enumerate(links_object.originals):
            self.originals.append(links_object.originals[i])
            self.formatted.append(links_object.formatted[i])
            self.names.append(links_object.names[i])
        for link in links_object.broken:
            self.broken.append(link)

    # If all the lists are empty, return True.
    def isEmpty(self):
        isempty = True
        if len(self.originals):
            isempty = False
        elif len(self.formatted):
            isempty = False
        elif len(self.names):
            isempty = False
        elif len(self.broken):
            isempty = False

        return isempty


# Get the absolute path of an asset with an unknown location.
# The location must be one of the asset_dir_paths.
def get_abspath(file_path):
    asset_dir_paths = settings.get_asset_dir_paths()
    for dir_path in asset_dir_paths:
        path = os.path.join(dir_path, file_path)
        if os.path.exists(path):
            return path
    return file_path


# Change the form of an asset link to make it easier to use.
# Broken links will not be made absolute.
def format_link(file_path):
    # Remove 'file://' from the beginning of any file links that have it.
    if file_path.startswith('file://'):
        file_path = file_path[7:]
    # Make any relative file links absolute.
    if not os.path.isabs(file_path):
        file_path = get_abspath(file_path)
    # Replace all instances of '\\' with '/'.
    file_path = file_path.replace('\\', '/')

    return file_path

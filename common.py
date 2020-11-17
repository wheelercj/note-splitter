# This file is code that is used by multiple other files, or may be in the future.

import os
import re

zettel_types = ('.md', '.markdown')
zettel_type_pattern = r'\.(md|markdown)'
asset_types = ('.jpg', '.jpeg', '.png', '.pdf', '.mp4', '.html')
asset_link_pattern = re.compile(r'(?<=(\(|\\|/))([^(\(|\\|/)]+)\.(jpg|jpeg|png|pdf|mp4|html)\)')


# Returns lists of the names of all zettels and assets in the zettelkasten.
def get_file_names():
    directory = os.listdir('..')
    zettel_names = get_zettel_names(directory)
    asset_names = get_asset_names(directory)

    return zettel_names, asset_names


# Parameter: a list of all files in the zettelkasten directory.
# Returns a list of the names of all zettels in the zettelkasten.
def get_zettel_names(directory):
    zettel_names = []
    for file_name in directory:
        if file_name.endswith(zettel_types):
            zettel_names.append(file_name)

    return zettel_names


# Parameter: a list of all files in the zettelkasten directory.
# Returns a list of the names of all assets in the zettelkasten.
def get_asset_names(directory):
    asset_names = []
    for file_name in directory:
        if file_name.endswith(asset_types):
            asset_names.append(file_name)

    return asset_names

# This file is code that is used by multiple other files, or may be in the future.

import os
import re

zettel_types = ('.md', '.markdown')
asset_types = ('.jpg', '.jpeg', '.png', '.pdf', '.mp4', '.html')
asset_link_pattern = re.compile(r'(?<=(\(|\\|/))([^(\(|\\|/)]+)\.(jpg|jpeg|png|pdf|mp4|html)\)')


# Returns lists of the names of all zettels and assets in the zettelkasten.
def get_file_names():
    zettel_names = []
    asset_names = []
    for file_name in os.listdir('..'):
        if file_name.endswith(zettel_types):
            zettel_names.append(file_name)
        elif file_name.endswith(asset_types):
            asset_names.append(file_name)

    return zettel_names, asset_names

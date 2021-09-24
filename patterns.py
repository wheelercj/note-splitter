# Resources for learning and using regex:
# https://wheelercj.github.io/notes/posts/20210506235005.html


import re


class patterns:
    """Compiled regex patterns."""
    any_header = re.compile(r'(^#+ .+)')  # A markdown header of any level.
    tags = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')  # For group[1] to be
        # a tag, group[0] must be in ('', ' ', '\t').

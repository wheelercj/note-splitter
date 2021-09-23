# Resources for learning and using regex:
# https://wheelercj.github.io/notes/20210506235005.html


import re


class patterns:
    """Compiled regex patterns."""
    any_header = re.compile(r'(^#+ .+)')
    tags = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')

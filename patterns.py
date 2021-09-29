# Resources for learning and using regex:
# https://wheelercj.github.io/notes/posts/20210506235005.html


import re


class patterns:
    """Compiled regex patterns as class attributes (not instance attributes).
    
    Attributes
    ----------
    any_header : Pattern
        The pattern of a markdown header of any level.
    tags : Pattern
        The pattern for a tag and the character before the tag. For 
        group[1] to be a tag, group[0] must be in ('', ' ', '\t').
    """
    any_header = re.compile(r'(^#+ .+)')
    tags = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')

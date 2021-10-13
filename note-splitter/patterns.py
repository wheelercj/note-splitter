r"""Compiled regular expressions.

Resources for learning and using regex: 
https://wheelercj.github.io/notes/posts/20210506235005.html

Attributes
----------
any_header : re.Pattern
    The pattern of a markdown header of any level.
tags : re.Pattern
    The pattern for a tag and the character before the tag. For 
    :code:`group[1]` to be a tag, :code:`group[0]` must be in 
    :code:`('', ' ', '\t')`.
"""


import re


any_header = re.compile(r'(^#+ .+)')
tags = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')

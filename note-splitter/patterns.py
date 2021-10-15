r"""Compiled regular expressions.

Resources for learning and using regex: 
https://wheelercj.github.io/notes/pages/20210506235005.html

Attributes
----------
any_header : re.Pattern
    The pattern of a markdown header of any level.
tags : re.Pattern
    The pattern for a tag and the character before the tag. For 
    :code:`group[1]` to be a tag, :code:`group[0]` must be in 
    :code:`('', ' ', '\t')`.
horizontal_rule : re.Pattern
    The pattern for a markdown-style horizontal rule, which is composed
    of three or more minuses, underscores, or asterisks. There may be 
    any number of whitespace characters anywhere on the line.
frontmatter_fence : re.Pattern
    The pattern for a frontmatter delimiter.
code_fence : re.Pattern
    The pattern for a multi-line code block delimiter; the line starts
    with either three backticks or three tildes.
"""


import re


any_header = re.compile(r'^#+ .+')
tags = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')
horizontal_rule = re.compile(r'\s*(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})')
frontmatter_fence = re.compile(r'^---$')
code_fence = re.compile(r'^(?:```|~~~).*')

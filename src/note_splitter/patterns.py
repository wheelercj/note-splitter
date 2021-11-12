r"""Compiled regular expressions.

Resources for learning and using regex: 
https://wheelercj.github.io/notes/pages/20210506235005.html

Most of these patterns are for full-line elements that are each
in their own string with no newline characters.

Attributes
----------
any_header : re.Pattern
    The pattern of a header of any level (a full-line element).
horizontal_rule : re.Pattern
    The pattern for a horizontal rule, which is composed of three or 
    more minuses, underscores, or asterisks. There may be any number of 
    whitespace characters anywhere on the line (a full-line element).
frontmatter_fence : re.Pattern
    The pattern for a frontmatter delimiter (a full-line element).
code_fence : re.Pattern
    The pattern for a multi-line code block delimiter (a full-line 
    element); the line starts with either three backticks or three 
    tildes.
math_fence : re.Pattern
    The pattern for the delimiter of a multi-line block of math 
    equations (a full-line element).
blockquote : re.Pattern
    The pattern for a quote that takes up one entire line (a full-line 
    element).
to_do : re.Pattern
    The pattern for a to do list item that is not completed (a full-line
    element).
footnote : re.Pattern
    The pattern for a footnote (a full-line element).
unordered_list_item : re.Pattern
    The pattern for an item in a bullet point list (a full-line 
    element). The list can have bullet points as asterisks, minuses, or 
    pluses. This pattern can also match some horizontal rules and to 
    dos.
ordered_list_item : re.Pattern
    The pattern for an item in an ordered list (a full-line element).
table_divider : re.Pattern
    The pattern for the part of a table that divides the table's header
    from its body (a full-line element). This pattern can also match 
    some horizontal rules.
table_row : re.Pattern
    The pattern for a row of a table (a full-line element). This pattern
    can also match some table dividers. Table rows that do not start and
    end with a pipe symbol are not supported.
tag : re.Pattern
    The pattern for a tag (an inline element).
"""
# This module follows the Global Object Pattern. You can see more 
# details about this design pattern here: 
# https://python-patterns.guide/python/module-globals/#id1


import re

# full-line elements
empty_line = re.compile(r'^\s*$')
any_header = re.compile(r'^#+ .+')
horizontal_rule = re.compile(r'^\s*(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})$')
frontmatter_fence = re.compile(r'^(?:---|\*\*\*)$')
code_fence = re.compile(r'^(?:```|~~~).*')
math_fence = re.compile(r'^\s*\$\$\s*$')
blockquote = re.compile(r'^(?:>\s*)+.+$')
to_do = re.compile(r'^\s*[*+-] \[[x\s]\] .+')
footnote = re.compile(r'^\[\^[^^\s\n][^^\n]*(?<!\s)\]: [^\n]+')
unordered_list_item = re.compile(r'^\s*[*+-]\s.*')
ordered_list_item = re.compile(r'^\s*\d+[.)]\s.*')
table_divider = re.compile(r'^\|?(?: *[-:]{3,} *\|?)+$')
table_row = re.compile(r'^\|.+\|$')

# inline elements
tag = re.compile(r'(?<!\S)(?:(?:#+[\w\d_-]*[\w\d_-]#?)|(?:(?<=.)#+[\w\d_-]*[\w\d_-]#?))')

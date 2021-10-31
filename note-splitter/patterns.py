r"""Compiled regular expressions.

Resources for learning and using regex: 
https://wheelercj.github.io/notes/pages/20210506235005.html

Attributes
----------
any_header : re.Pattern
    The pattern of a markdown header of any level.
tags : re.Pattern
    The pattern for a tag and the character before the tag. For 
    :code:`group[1]` to be a tag, :code:`group[0]` must be 
    :code:`in ('', ' ', '\t')`.
horizontal_rule : re.Pattern
    The pattern for a markdown-style horizontal rule, which is composed
    of three or more minuses, underscores, or asterisks. There may be 
    any number of whitespace characters anywhere on the line.
frontmatter_fence : re.Pattern
    The pattern for a frontmatter delimiter.
code_fence : re.Pattern
    The pattern for a multi-line code block delimiter; the line starts
    with either three backticks or three tildes.
math_fence : re.Pattern
    The pattern for the delimiter of a multi-line block of math 
    equations.
blockquote : re.Pattern
    The pattern for a quote that takes up one entire line.
to_do : re.Pattern
    The pattern for a to do list item that is not completed.
done : re.Pattern
    The pattern for a to do list item that is completed.
footnote : re.Pattern
    The pattern for a footnote (the ones usually at the bottom of a 
    file, not their references).
ordered_list_item : re.Pattern
    The pattern for an item in a numbered list.
unordered_list_item : re.Pattern
    The pattern for an item in a bullet point list. The list can have 
    bullet points as asterisks, minuses, or pluses.
table_divider : re.Pattern
    The pattern for the part of a table that divides the table's header
    from its body.
table_row : re.Pattern
    The pattern for a row of a table. This pattern matches all strings
    that match the table divider pattern, so when looking for table 
    rows, first make sure it's not a table divider.
"""


import re


empty_line = re.compile(r'^\s*$')
any_header = re.compile(r'^#+ .+')
tags = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')
horizontal_rule = re.compile(r'\s*(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})')
frontmatter_fence = re.compile(r'^---$')
code_fence = re.compile(r'^(?:```|~~~).*')
math_fence = re.compile(r'.*\$\$\s*')
blockquote = re.compile(r'^>+ .+')
to_do = re.compile(r'^- \[ \] .+')
done = re.compile(r'^- \[x\] .+')
footnote = re.compile(r'^\[\^.+\]: .+')
ordered_list_item = re.compile(r'\s*\d+\.\s+[^\s].*')
unordered_list_item = re.compile(r'\s*[*\-\+] [^\s].*')
table_divider = re.compile(r'^\|(?: +:?\-+:? +\|)+$')
table_row = re.compile(r'^\| .+ \|$')

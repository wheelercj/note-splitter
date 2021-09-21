# Splits raw markdown into tokens.

# Token types:
#   frontmatter: str
#   codeblock: Dict[str, str]
#   global tags: List[str]
#   header: Dict[str, Union[int, str]]
#   text: str

# Frontmatter must be at the top of the file, or have only empty lines
# above it. Frontmatter always begins with '---' and ends with '---'.
# Global tags are tags that are not below any header of level 2+.
# There should only be a maximum of one frontmatter token and one global
# tags token per file.

# Here's an explanation of how to create a token list and an AST:
# https://www.twilio.com/blog/abstract-syntax-trees


import re
from typing import List, Tuple, Any


class Token:
    def __init__(self, _type: str, content: Any):
        self._type = _type
        self.content = content


def md_to_tokens(markdown: str) -> List[Token]:
    """Converts raw markdown into a list of tokens."""
    tokens: List[Token] = []

    # There can only be one frontmatter token and one global tags token
    # per file, and frontmatter and global tags can only be in certain
    # parts of each file.
    can_find_frontmatter = True
    can_find_global_tags = True

    # Frontmatter and codeblocks can span multiple lines, so we need to 
    # keep track of whether we're in one of those since files are parsed
    # one line at a time.
    in_frontmatter = False
    in_codeblock = False

    frontmatter_contents = ''
    global_tags: List[str] = []
    codeblock = {
        'language': '',
        'content': ''
    }

    header_pattern = re.compile(r'(^#{1,6} .+)')  
        # TODO: support underline headers?
    tag_pattern = re.compile(r'(.|\B)(#[a-zA-Z0-9_-]+)')

    for line in markdown.split('\n'):
        if can_find_frontmatter and line.startswith('---'):
            in_frontmatter = True
        else:
            if line != '':
                can_find_frontmatter = False

            if in_frontmatter:
                if line.startswith('---'):
                    in_frontmatter = False
                    tokens.append(Token('frontmatter', frontmatter_contents))
                else:
                    frontmatter_contents += line
            elif in_codeblock:
                if line.startswith('```'):
                    in_codeblock = False
                    tokens.append(Token('codeblock', codeblock))
                    codeblock = {'language': '', 'content': ''}
                else:
                    codeblock['content'] += line
            elif line.startswith('```'):
                in_codeblock = True
                codeblock['language'] = line.lstrip('`').strip()
            else:
                header_match: re.Match = header_pattern.match(line)
                if header_match:
                    header = header_match[0]
                    header_content = header.lstrip('#')
                    header_level = len(header) - len(header_content)
                    header_content = header_content.lstrip()
                    tokens.append(Token(
                        'header', {
                            'level': header_level,
                            'content': header_content
                        }))
                    if header_level > 1:
                        can_find_global_tags = False
                else:
                    tokens.append(Token('text', line))
                if can_find_global_tags:
                    tag_groups: List[Tuple[str]] = tag_pattern.findall(line)
                    for group in tag_groups:
                        if not group[0] or group[0] == ' ':
                            global_tags.append(group[1])
    
    tokens.append(Token('global tags', global_tags))
    return tokens

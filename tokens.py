# Splits raw text into a list of tokens.

# Token types:
#   frontmatter: str
#   codeblock: Dict[str, str]
#   global tags: List[str]
#   header: Dict[str, Union[int, str]]
#   text: str

# TODO: find out other tokens commonly needed by researchers, and 
# whether we will need to make a separate token for each line of 
# frontmatter.

# Here are guides for token lists, ASTs, and lexical analysis:
# https://www.twilio.com/blog/abstract-syntax-trees
# https://en.wikipedia.org/wiki/Lexical_analysis
# https://craftinginterpreters.com/scanning.html

# Frontmatter must be at the top of the file, or have only empty lines
# above it. Frontmatter always begins and ends with a line of '---'.
# Global tags are tags that are not below any header of level 2+.
# There should only be a maximum of one frontmatter token and one global
# tags token per file.


# external imports
from typing import List, Tuple, Any

# internal imports
from patterns import patterns


class Token:
    def __init__(self, _type: str, content: Any):
        self._type = _type
        self.content = content


class Lexer:
    """Creates a Callable that converts raw text to a list of tokens
    
    The Callable can be used multiple times.
    """

    def __call__(self, text: str) -> List[Token]:
        """Converts raw text to a list of tokens."""
        self.tokens: List[Token] = []
        self.lines = text.split('\n')
        self.line_number = 0
        self.global_tags: List[str] = []
        
        # There can only be one frontmatter token and one global tags 
        # token per file, and frontmatter and global tags can only be in
        # certain parts of each file.
        self.can_find_frontmatter = True
        self.can_find_global_tags = True

        try:
            self.tokenize()
        except StopIteration:
            if self.global_tags:
                self.append_global_tags_token()
            return self.tokens


    def get_next_line(self) -> str:
        """Gets the next line in the given text
        
        Increments self.line_number. Raises StopIteration if the end of 
        the text is reached.
        """
        try:
            line = self.lines[self.line_number]
        except IndexError:
            raise StopIteration
        else:
            self.line_number += 1
            return line


    def tokenize(self) -> None:
        """Converts raw text to a list of tokens
        
        Raises StopIteration when the end of the text is reached.
        """
        while True:
            line = self.get_next_line()
            self.append_token(line)
            if self.can_find_global_tags:
                self.find_all_tags(line)
            if line != '':
                self.can_find_frontmatter = False


    def append_token(self, line: str) -> None:
        """Parses the text and appends the next token
        
        Raises StopIteration if the end of the text is reached.
        """
        if self.is_frontmatter(line):
            self.append_frontmatter_token()
        elif self.is_codeblock(line):
            self.append_codeblock_token(line)
        elif self.is_any_header(line):
            self.append_header_token(line)
        else:
            self.append_text_token(line)


    def is_frontmatter(self, line: str) -> bool:
        """Determines if the line is the beginning of frontmatter."""
        return self.can_find_frontmatter and line == '---'


    def is_codeblock(self, line: str) -> bool:
        """Determines if the line is the beginning of a codeblock."""
        return line.startswith('```')


    def is_any_header(self, line: str) -> bool:
        """Determines if the line is a header of any level."""
        return bool(patterns.any_header.match(line))


    def append_frontmatter_token(self) -> None:
        """Parses and appends a frontmatter token
        
        Raises StopIteration if the end of the text is reached.
        """
        frontmatter_contents = ''
        while True:
            line = self.get_next_line()
            if line == '---':
                self.tokens.append(Token('frontmatter', frontmatter_contents))
                return
            else:
                frontmatter_contents += line + '\n'


    def append_codeblock_token(self, line: str) -> None:
        """Parses and appends a codeblock token
        
        Raises StopIteration if the end of the text is reached.
        """
        codeblock = { 'language': '', 'content': '' }
        codeblock['language'] = line.lstrip('`').strip()

        while True:
            line = self.get_next_line()
            if line.startswith('```'):
                self.tokens.append(Token('codeblock', codeblock))
                return
            else:
                codeblock['content'] += line + '\n'


    def append_header_token(self, line: str) -> None:
        """Parses and appends a header token
        
        Also updates self.can_find_global_tags if necessary.
        """
        header_content = line.lstrip('#')
        header_level = len(line) - len(header_content)
        header_content = header_content.lstrip()
        self.tokens.append(Token(
            'header', {
                'level': header_level,
                'content': header_content
            }))
        if header_level > 1:
            self.can_find_global_tags = False


    def append_text_token(self, line: str) -> None:
        """Appends a text token."""
        self.tokens.append(Token('text', line))


    def find_all_tags(self, line: str) -> None:
        """Finds and appends any tags to the global_tags list."""
        tag_groups: List[Tuple[str]] = patterns.tags.findall(line)
        for group in tag_groups:
            if group[0] in ('', ' ', '\t'):
                self.global_tags.append(group[1])


    def append_global_tags_token(self) -> None:
        """Appends a global tags token."""
        self.tokens.append(Token('global tags', self.global_tags))

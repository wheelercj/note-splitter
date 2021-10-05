# Splits raw text into a list of tokens.

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
    """Creates a Callable that converts raw text to a list of tokens.
    
    token types
    -----------
    frontmatter : str
    codeblock : Dict[str, str]
    global tags : List[str]
    header : Dict[str, Union[int, str]]
    text : str
    """

    def __call__(self, text: str) -> List[Token]:
        """Converts raw text to a list of tokens."""
        self.tokens: List[Token] = []
        self.lines = text.split('\n')
        self.line_number = 0
        self.global_tags: List[str] = []
        
        # There can be a maximum of only one frontmatter token and one 
        # global tags token per file, and frontmatter and global tags 
        # can only be in certain parts of each file.
        self.can_find_frontmatter = True
        self.can_find_global_tags = True

        try:
            self.__tokenize()
        except StopIteration:
            if self.global_tags:
                self.__append_global_tags_token()
            return self.tokens


    def __get_next_line(self) -> str:
        """Gets the next line in the text.
        
        Raises
        ------
        StopIteration
            If the end of the text is reached.
        """
        try:
            line = self.lines[self.line_number]
        except IndexError:
            raise StopIteration
        else:
            self.line_number += 1
            return line


    def __tokenize(self) -> None:
        """Converts raw text to a list of tokens.
        
        Raises
        ------
        StopIteration
            When the end of the text is reached.
        """
        while True:
            line = self.__get_next_line()
            self.__append_token(line)
            if self.can_find_global_tags:
                self.__find_all_tags(line)
            if line != '':
                self.can_find_frontmatter = False


    def __append_token(self, line: str) -> None:
        """Parses the text and appends the next token.
        
        Raises
        ------
        StopIteration
            If the end of the text is reached.
        """
        if self.__is_frontmatter(line):
            self.__append_frontmatter_token()
        elif self.__is_codeblock(line):
            self.__append_codeblock_token(line)
        elif self.__is_any_header(line):
            self.__append_header_token(line)
        else:
            self.__append_text_token(line)


    def __is_frontmatter(self, line: str) -> bool:
        """Determines if the line is the beginning of frontmatter."""
        return self.can_find_frontmatter and line == '---'


    def __is_codeblock(self, line: str) -> bool:
        """Determines if the line is the beginning of a codeblock."""
        return line.startswith('```')


    def __is_any_header(self, line: str) -> bool:
        """Determines if the line is a header of any level."""
        return bool(patterns.any_header.match(line))


    def __append_frontmatter_token(self) -> None:
        """Parses and appends a frontmatter token.
        
        Raises
        ------
        StopIteration
            If the end of the text is reached.
        """
        frontmatter_contents = ''
        while True:
            line = self.__get_next_line()
            if line == '---':
                self.tokens.append(Token('frontmatter', frontmatter_contents))
                return
            else:
                frontmatter_contents += line + '\n'


    def __append_codeblock_token(self, line: str) -> None:
        """Parses and appends a codeblock token.
        
        Raises
        ------
        StopIteration
            If the end of the text is reached.
        """
        codeblock = { 'language': '', 'content': '' }
        codeblock['language'] = line.lstrip('`').strip()

        while True:
            line = self.__get_next_line()
            if line.startswith('```'):
                self.tokens.append(Token('codeblock', codeblock))
                return
            else:
                codeblock['content'] += line + '\n'


    def __append_header_token(self, line: str) -> None:
        """Parses and appends a header token.
        
        Also determines whether it is still possible to find global 
        tags.
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


    def __append_text_token(self, line: str) -> None:
        """Appends a text token."""
        self.tokens.append(Token('text', line))


    def __find_all_tags(self, line: str) -> None:
        """Finds and appends any tags to the global tags list."""
        tag_groups: List[Tuple[str]] = patterns.tags.findall(line)
        for group in tag_groups:
            if group[0] in ('', ' ', '\t'):
                self.global_tags.append(group[1])


    def __append_global_tags_token(self) -> None:
        """Appends a global tags token."""
        self.tokens.append(Token('global tags', self.global_tags))

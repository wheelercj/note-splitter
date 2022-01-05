"""For splitting an AST's tokens into Sections tokens."""


from typing import List, Tuple
from note_splitter import tokens, patterns
from note_splitter.settings import settings


class Splitter:
    """Creates a Callable that splits a token list into Sections."""

    def __call__(
            self,
            tokens_: List[tokens.Token]) \
            -> Tuple[List[tokens.Section], List[str]]:
        """Splits a tokens list into Sections.

        Parameters
        ----------
        tokens_ : List[tokens.Token]
            A list of tokens to split.
        
        Returns
        -------
        sections : List[tokens.Section]
            A list of the sections created by splitting. These are like 
            smaller ASTs.
        global_tags : List[str]
            A list of the tags that are not in any of the sections.
        """
        self.__tokens = tokens_
        sections, global_tags = self.__get_sections()
        return sections, global_tags


    def __get_sections(self) -> Tuple[List[tokens.Section], List[str]]:
        """Groups the tokens into section tokens.

        Returns
        -------
        sections : List[tokens.Section]
            A list of the sections created by splitting. These are like
            smaller ASTs.
        global_tags : List[str]
            A list of the tags that are not in any of the sections.
        """
        # Depth-first search for tokens of the chosen split type.
        # Irrelevant tokens are deleted as the loop iterates.
        sections: List[tokens.Section] = []
        global_tags: List[str] = []
        while self.__tokens:
            token = self.__tokens[0]
            if settings['using_split_keyword'] \
                    and settings['remove_split_keyword'] \
                    and isinstance(token, tokens.CanHaveInlineElements) \
                    and settings['split_keyword'] in token.content:
                token.content = token.content.replace(
                    settings['split_keyword'], '')
                if not token.content:
                    self.__tokens.pop(0)
                    continue
            if self.__should_split(
                    token,
                    is_splitting=False):
                new_section = self.__get_section()
                sections.append(new_section)
            elif isinstance(token.content, list):
                split = Splitter()
                new_sections, new_global_tags = split(token.content)
                sections.extend(new_sections)
                global_tags.extend(new_global_tags)
                self.__tokens.pop(0)
            else:
                if isinstance(token, tokens.CanHaveInlineElements):
                    tags = patterns.tag.findall(token.content)
                    global_tags.extend(tags)
                self.__tokens.pop(0)

        return sections, global_tags


    def __get_section(self) -> tokens.Section:
        """Groups some of the tokens into one new section token.
        
        Assumes the first token in the tokens list is of the type that
        was chosen to split by.
        
        If the token type chosen as the section starter has
        a ``level`` attribute, it must be an integer and lower 
        levels will take precedence over higher levels. E.g., each 
        header token has a level, and larger headers have smaller 
        levels (the largest header possible has a level of 1). When a 
        file is split by headers of level 2, each section (each new 
        file) will start with a header of level 2 and will not contain 
        any other headers of level 2 or any of level 1, but may contain 
        headers of level 3 or greater.
        """
        section_tokens: List[tokens.Token] = []
        section_tokens.append(self.__tokens.pop(0))

        while self.__tokens:
            token = self.__tokens[0]
            if self.__should_split(token):
                return tokens.Section(section_tokens)
            else:
                section_tokens.append(token)
                self.__tokens.pop(0)

        return tokens.Section(section_tokens)


    def __should_split(
            self,
            token: tokens.Token,
            is_splitting: bool = True) -> bool:
        """Determines if a token has certain attributes and values.

        Assumes the token is of the type that was chosen to split by,
        and that the split attributes exist.

        Parameters
        ----------
        token : tokens.Token
            A token that may be of the type chosen to split by.
        is_splitting : bool
            A boolean for whether splitting is in progress. Used to 
            determine if the tokens should be split just before a token 
            of a lower level than the chosen split level. True by 
            default.
        """
        if not isinstance(token, settings['split_type']):
            return False
        if settings['split_attrs'] \
                and list(settings['split_attrs'])[0] \
                and (list(settings['split_attrs'].values())[0] \
                or list(settings['split_attrs'].values())[0] == 0):
            for key, value in settings['split_attrs'].items():
                if isinstance(value, str) and value.isnumeric():
                    value = int(value)
                if is_splitting and key == 'level':
                    if token.level > value:
                        return False
                elif key is not None and getattr(token, key) != value:
                    return False
        return True

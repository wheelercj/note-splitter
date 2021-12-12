"""For changing some important details in Section tokens before output.

The Formatter class' callable normalizes header levels, adds frontmatter
and global tags to each section, and then converts the section tokens to
strings.
"""


from typing import List, Optional
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation
from note_splitter import tokens


class Formatter:
    """Creates a Callable that prepares sections for output.
    
    The callable normalizes header levels, adds frontmatter and global 
    tags to each section, and then converts the section tokens to
    strings.
    """

    def __call__(
            self,
            sections: List[tokens.Section],
            global_tags: List[str],
            frontmatter: Optional[object] = None) -> List[str]:
        """Formats sections for output.
        
        Parameters
        ----------
        sections : List[tokens.Section]
            The sections to format.
        global_tags : List[str]
            The global tags to add to each section.
        frontmatter : Optional[object]
            The frontmatter to add to each section.
        """
        split_contents: List[str] = []
        for section in sections:
            if not section.content:
                continue
            if isinstance(section.content[0], tokens.Header):
                section_title = self.normalize_headers(section)
            self.insert_global_tags(global_tags, section)
            self.prepend_frontmatter(frontmatter, section_title, section)
            split_contents.append(str(section))
        return split_contents


    def normalize_headers(self, section: tokens.Section) -> str:
        """Normalizes the markdown header levels in a section.
        
        Parameters
        ----------
        section : tokens.Section
            The section to normalize.

        Returns
        -------
        str
            The title of the section.
        """
        first_token = section.content[0]
        if first_token.level <= 1:
            return first_token.body
        difference = first_token.level - 1
        for i, token in enumerate(section.content):
            if isinstance(token, tokens.Header):
                section.content[i].level -= difference
                section.content[i].content = \
                    section.content[i].content[difference:]
        return first_token.body


    def insert_global_tags(self,
                           global_tags: List[str], 
                           section: tokens.Section) -> None:
        """Inserts the global tags into a section.
        
        Parameters
        ----------
        global_tags : List[str]
            The global tags to add to the section.
        section : tokens.Section
            The section to insert the global tags into.
        """
        i = 0
        while i < len(section.content) \
                and not isinstance(section.content[i], tokens.Header):
            i += 1
        i += 1
        if i < len(section.content):
            section.content.insert(i, tokens.Text(' '.join(global_tags)))
        else:
            section.content.insert(0, tokens.Text(' '.join(global_tags)))


    def prepend_frontmatter(self,
                            frontmatter: Optional[object],
                            section_title: str,
                            section: tokens.Section) -> None:
        """Prepends the frontmatter to a section.
        
        Parameters
        ----------
        frontmatter : Optional[object]
            The frontmatter to add to the section.
        section_title : str
            The title of the section.
        section : tokens.Section
            The section to prepend the frontmatter to.
        """
        if not frontmatter:
            return
        if isinstance(frontmatter, dict):
            if 'title' in frontmatter:
                frontmatter['title'] = section_title
        frontmatter_string = yaml.dump(frontmatter)
        frontmatter_string = '---\n' + frontmatter_string + '---\n'
        frontmatter_string = frontmatter_string.replace('\n\n', '\n')
        section.content.insert(0, tokens.Text(frontmatter_string))

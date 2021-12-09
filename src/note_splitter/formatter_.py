"""For changing some important details in Section tokens before output.

The Formatter class' callable normalizes header levels, adds frontmatter
and global tags to each section, and then converts the section tokens to
strings.
"""


from typing import List, Optional
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation
from note_splitter import settings, tokens


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
        if settings.split_type == tokens.Header:
            check_for_level = False
            difference_level = 0
            for i, each in enumerate(sections):
                # normalize the headers
                each.content[0].content = each.content[0].content.replace('#', '')
                if i == 0:
                    if each.content[0].level > 1:
                        difference_level = each.content[0].level - 1
                        each.content[0].level -= difference_level
                        check_for_level = True
                else:
                    if check_for_level:
                        each.content[0].level -= difference_level
                if each.content[0].level < 1:
                    each.content[0].level = 1
                each.content[0].content = '#' * each.content[0].level + each.content[0].content

        if isinstance(frontmatter, dict):
            if 'title' in frontmatter:
                frontmatter['new_name'] = frontmatter.pop('title')
        frontmatter_string = yaml.dump(frontmatter)
        
        # insert the frontmatter and global tags into each section
        if frontmatter:
            for i in range(len(sections)):
                sections[i].content = ['---\n' + frontmatter_string + '---\n'] + global_tags + sections[i].content
        else:
            for i in range(len(sections)):
                if sections[i].content[0] == tokens.Header:
                    sections[i].content = [sections[i].content[0]] + global_tags + sections[i].content[1:]
                else:
                    sections[i].content = global_tags + sections[i].content

        for each in sections:
            split_contents.append(str(each))
        return split_contents

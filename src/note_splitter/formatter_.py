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

        # TODO: normalize the headers in each section.
        # if the split type (settings.split_type) is tokens.Header:
        #   for each section:
        #       if the section's first token (a header) has a level greater than 1:
        #           then reduce the level of all headers in the section equally so that the first header has a level of 1

        # TODO: Insert the frontmatter and global tags into each section.
        #   The frontmatter may be any standard Python object (dict, list, etc.).
        #   If the frontmatter is a dictionary with a 'title' key, then that key's value will need to be changed to whatever the new file's title will be.
        #       We can just use placeholder names for now.
        #   We can convert Python objects back to YAML with `frontmatter_string = yaml.dump(frontmatter_object)`.
        #   If there is frontmatter, it should be inserted at the very top of the file, surrounded by lines containing only '---'.
        #   The global tags should be inserted under the first header, if there is one. Otherwise, they should be inserted under at the top of the file (under frontmatter if it's there).

        # TODO: convert the sections to strings and return them.
        #  * For each section, combine its tokens into one string (use `str(section)`).
        #  * Then each string in the split_contents list will be from one section.
        return split_contents

        # See test.py for an example of how this class can be used.

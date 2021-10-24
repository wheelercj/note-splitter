"""For changing some details in Section tokens before output."""


# external imports
from typing import List, Optional
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation

# internal imports
import settings
import tokens


class Formatter:
    """Creates a Callable that prepares section tokens for output."""

    def __call__(
            self,
            sections: List[tokens.Section],
            global_tags: List[str],
            frontmatter: Optional[object] = None) -> List[str]:
        """"""
        split_contents: List[str] = []

        # ...

        return split_contents


        # TODO: 
        # if the split type (the type of the first token in all of the sections) is tokens.Header:
        #   if the header has a level besides 1:
        #       then reduce all headers in the section equally so that the first header has a level of 1

        # TODO:
        # Insert the frontmatter and global tags from the AST into each section.
        #   If the frontmatter is a dictionary with a 'title' key, then that key's value will need to be changed to whatever the new file's title will be.
        #   We can convert Python objects back to YAML with `frontmatter_string = yaml.dump(frontmatter_object)`.
        #   If there is frontmatter, it should go at the very top of the file. 
        #   The global tags should go under the first header.

        # TODO:
        # For each section, combine its tokens into one string.
        # Each string in the split_contents list will be from one section.

        # See test.py for an example of how this class can be used.

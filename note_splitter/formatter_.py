"""For changing some important details in Section tokens before output.

The Formatter class' callable normalizes header levels, adds frontmatter
and global tags to each section, and then converts the section tokens to
strings.
"""

# external imports
from typing import List, Optional
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation

# internal imports
import settings
import tokens


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
        if settings.split_type == tokens.Header:
            #   for each section:
            check_for_level = False
            difference_level = 0
            for i, each in enumerate(sections):
                # print(f"{i} - beofre", each.content[0].level)
                # if the section's first token (a header) has a level greater than 1:
                #   then reduce the level of all headers in the section equally so that the first header has a level of 1
                if i == 0:
                    if each.content[0].level > 1:
                        difference_level = each.content[0].level - 1
                        each.content[0].level -= difference_level
                        check_for_level = True
                else:
                    if check_for_level:
                        each.content[0].level -= difference_level

                # print(f"{i} - aftter", each.content[0].level)
        # for each in sections:
        #     print("gg", each.content[0].level)
        # TODO: Insert the frontmatter and global tags into each section.
        #   The frontmatter may be any standard Python object (dict, list, etc.).
        #   If the frontmatter is a dictionary with a 'title' key, then that key's value will need to be changed to whatever the new file's title will be.
        #       We can just use placeholder names for now.
        if isinstance(frontmatter, dict):
            if "title" in frontmatter:
                frontmatter["new_name"] = frontmatter.pop('title')
        #   We can convert Python objects back to YAML with `frontmatter_string = yaml.dump(frontmatter_object)`.
        frontmatter_string = yaml.dump(frontmatter)
        # print("efwgfwgdfwefc", frontmatter_string, type(frontmatter_string))
        #   If there is frontmatter, it should be inserted at the very top of the file, surrounded by lines
        #   containing only '---'.
        if frontmatter:
            for i in range(len(sections)):
                sections[i].content = ["---\n" + frontmatter_string + "---\n"] + sections[i].content
        #   The global tags should be inserted under the first header, if there is one. Otherwise, they should be
        #   inserted under at the top of the file (under frontmatter if it's there).

        # TODO: convert the sections to strings and return them.
        #  * For each section, combine its tokens into one string (use `str(section)`).
        #  * Then each string in the split_contents list will be from one section.
        for each in sections:
            split_contents.append(str(each))
        return split_contents

        # See test.py for an example of how this class can be used.

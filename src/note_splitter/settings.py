"""The user's application settings and related functions.

The settings are stored in a dictionary named ``settings`` with the 
following keys. Some of these settings may be hidden from the user.

create_backlinks : bool
    Whether or not to append a backlink to the source file in each new 
    file.
blockquote_pattern : str
    The uncompiled regex pattern for blockquotes.
code_fence_pattern : str
    The uncompiled regex pattern for code fences.
copy_frontmatter : bool
    Whether or not to copy frontmatter from the source file to each new 
    file.
copy_global_tags : bool
    Whether or not to copy global tags from the source file to each new 
    file.
create_index_file : bool
    Whether or not to create an index file.
destination_folder_path : str
    The absolute path to the user's folder where new files will be 
    saved.
empty_line_pattern : str
    The uncompiled regex pattern for empty lines.
file_id_format : str
    The format of the file IDs.
file_id_regex : str
    The uncompiled regular expression to use to extract file IDs from 
    the files.
file_name_format : str
    The format of the new file names.
file_path_in_link_pattern : str
    The uncompiled regex pattern for file paths in links.
finished_task_pattern : str
    The uncompiled regex pattern for finished tasks.
footnote_pattern : str
    The uncompiled regex pattern for footnotes.
frontmatter_fence_pattern : str
    The uncompiled regex pattern for frontmatter fences.
header_pattern : str
    The uncompiled regex pattern for headers.
horizontal_rule_pattern : str
    The uncompiled regex pattern for horizontal rules.
math_fence_pattern : str
    The uncompiled regex pattern for math fences.
move_footnotes : bool
    Whether or not to copy footnotes into each new file that has the 
    relevant footnote references, and remove them from the ones that 
    don't have the relevant references.
note_types : List[str]
    The file extensions of the files that may be chosen to be split.Each
    must start with a period.
ordered_list_item_pattern : str
    The uncompiled regex pattern for ordered list items.
parse_blocks : bool
    Whether or not to create ``Block`` tokens while parsing.
remove_split_keyword : bool
    Whether or not to remove the split keyword from the source file and 
    new file(s).
replace_split_contents : bool
    Whether or not to replace the parts of the source file that was 
    split out with links to the new files.
source_folder_path : str
    The absolute path to the user's folder containing the files to be 
    split.
split_attrs : dict
    The attributes to split by. If the chosen split type has an 
    attribute, it can be used to narrow down what to split by.
split_keyword : str
    The tag/keyword the program searches for to know which file(s) to 
    split.
split_type : Type
    The type to split by. This can be any token type, even an abstract 
    one.
table_divider_pattern : str
    The uncompiled regex pattern for table dividers.
table_row_pattern : str
    The uncompiled regex pattern for table rows.
tag_pattern : str
    The uncompiled regex pattern for tags.
task_pattern : str
    The uncompiled regex pattern for tasks.
unordered_list_item_pattern : str
    The uncompiled regex pattern for unordered list items.
using_split_keyword : bool
    Whether or not the split keyword was used to find file(s) to split.

The settings for the formats of file names and IDs can use the following
variables:

 * ``%uuid4`` - A universally unique identifier.
 * ``%title`` - The title of the file (the body of its first header, or 
   the first line of the file if there is no header).
 * ``%Y`` - The current year.
 * ``%M`` - The current month.
 * ``%D`` - The current day.
 * ``%h`` - The current hour.
 * ``%m`` - The current minute.
 * ``%s`` - The current second.

Additionally, the file name format setting can use the ``%id`` variable 
which gets replaced with the ID of the file as described by the file ID 
format setting.

Every time file_id_format is changed, file_id_regex must be updated.
"""


from note_splitter import patterns
from note_splitter import tokens
from typing import Callable
from typing import List
from typing import Type
import json


__DEFAULT_SETTINGS = {
    "create_backlinks": False,
    "blockquote_pattern": patterns.blockquote.pattern,
    "code_fence_pattern": patterns.code_fence.pattern,
    "copy_frontmatter": False,
    "copy_global_tags": False,
    "create_index_file": True,
    "destination_folder_path": "",
    "empty_line_pattern": patterns.empty_line.pattern,
    "file_id_format": r"%Y%M%D%h%m%s",
    "file_id_regex": r"\d{14}",
    "file_name_format": r"%id",
    "file_path_in_link_pattern": patterns.file_path_in_link.pattern,
    "finished_task_pattern": patterns.finished_task.pattern,
    "footnote_pattern": patterns.footnote.pattern,
    "frontmatter_fence_pattern": patterns.frontmatter_fence.pattern,
    "header_pattern": patterns.header.pattern,
    "horizontal_rule_pattern": patterns.horizontal_rule.pattern,
    "math_fence_pattern": patterns.math_fence.pattern,
    "move_footnotes": False,
    "note_types": [".md", ".markdown", ".txt"],
    "ordered_list_item_pattern": patterns.ordered_list_item.pattern,
    "parse_blocks": True,
    "remove_split_keyword": True,
    "replace_split_contents": False,
    "source_folder_path": "",
    "split_attrs": {"level": 2},
    "split_keyword": "#split",
    "split_type": tokens.Header,
    "table_divider_pattern": patterns.table_divider.pattern,
    "table_row_pattern": patterns.table_row.pattern,
    "tag_pattern": patterns.tag.pattern,
    "task_pattern": patterns.task.pattern,
    "unordered_list_item_pattern": patterns.unordered_list_item.pattern,
    "using_split_keyword": True,
}


settings = {}


def save_settings() -> None:
    """Save the settings to a JSON file."""
    split_type: Type = settings["split_type"]
    settings["split_type"] = get_token_type_name(settings["split_type"])
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)
    settings["split_type"] = split_type


def load_settings() -> None:
    """Attempt to load the settings from a JSON file.

    If the file does not exist or cannot be decoded, the default
    settings are used.
    """
    try:
        with open("settings.json", "r") as file:
            settings.update(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        settings.update(__DEFAULT_SETTINGS)
    else:
        if "null" in settings["split_attrs"]:
            settings["split_attrs"] = {None: ""}
        settings["split_type"] = get_token_type(settings["split_type"])
        add_new_settings()


def add_new_settings() -> None:
    """Add any new settings to the settings file."""
    for key, value in __DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value


def reset_settings() -> None:
    """Reset the settings to their defaults."""
    settings.clear()
    settings.update(__DEFAULT_SETTINGS)


def get_token_type_names(
    filter_predicate: Callable[[Type], bool] = None, all_token_types: List[Type] = None
) -> List[str]:
    """Get all token types' output-formatted names.

    Parameters
    ----------
    predicate : Callable, optional
        A function that filters the token types.
    all_token_types : List, optional
        A list of all token types. If not provided, the list of all
        token types will be fetched.
    """
    if not all_token_types:
        all_token_types: List[Type] = tokens.get_all_token_types(tokens)
    token_names = []
    for token_type in all_token_types:
        if not filter_predicate or filter_predicate(token_type):
            token_names.append(get_token_type_name(token_type))
    return token_names


def get_token_type_name(token_type: Type) -> str:
    """Get the token type's output-formatted name.

    Parameters
    ----------
    token_type : Type
        The token type to get the name of.
    """
    token_name = []
    try:
        for i, letter in enumerate(token_type.__name__):
            if i and letter.isupper():
                token_name.append(" ")
            token_name.append(letter)
    except AttributeError:
        raise TypeError(f"{token_type} is not a Type.")
    return "".join(token_name).lower()


def get_token_type(chosen_name: str) -> Type:
    """Get a token type by name.

    Parameters
    ----------
    chosen_name : str
        The output-formatted name of the token type to get.
    """
    all_token_types: List[Type] = tokens.get_all_token_types(tokens)
    token_type_names = get_token_type_names(None, all_token_types)
    for name, type_ in zip(token_type_names, all_token_types):
        if name == chosen_name:
            return type_
    raise ValueError(f'Token type "{chosen_name}" not found.')

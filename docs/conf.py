"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# flake8: noqa: E402
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import inspect
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

from note_splitter import tokens


# -- Project information -----------------------------------------------------

project = "note splitter"
master_doc = "index"
copyright = (
    "2021, Chris Wheeler, Shiva Ramezani, Christian Vargas, and Serge Nazaretyan"
)
author = "C. Wheeler, S. Ramezani, C. Vargas, and S. Nazaretyan"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_include_init_with_doc = True

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: list[str] = []


# -- Custom automatic documentation ------------------------------------------

# This script overwrites token-hierarchy.rst with the token hierarchy.
# The current token hierarchy is determined automatically from the code.
# Run this each time you add a new token or change their relationships.
# More indentation in the hierarchy means that the token is a child of the
# previous token with less indentation.


def save_token_hierarchy():
    """Detects, creates, and saves the token hierarchy to a file."""
    token_hierarchy: str = create_token_hierarchy()
    with open("token-hierarchy.rst", "w") as file:
        file.write(token_hierarchy)
    print("Token hierarchy saved to docs/token-hierarchy.rst")


def create_token_hierarchy() -> str:
    """Detects and creates the entire token hierarchy as a string."""
    token_hierarchy = [
        "token hierarchy",
        "===============",
        "\nBelow is the hierarchy of all the tokens this program uses. More "
        "indentation means that the token is a child of the previous token "
        "with less indentation. Note that some of the token types inherit "
        "multiple others, so they are listed twice.\n",
    ]

    all_token_types = tokens.get_all_token_types(tokens)
    class_tree = inspect.getclasstree(all_token_types)
    __create_token_subhierarchy(token_hierarchy, class_tree)
    token_hierarchy.append("")
    return "\n".join(token_hierarchy)


def __create_token_subhierarchy(
    token_hierarchy: list[str], class_tree: list, indentation: str = ""
) -> None:
    """Creates part of the token hierarchy.

    The result is returned by reference.
    """
    for c in class_tree:
        if isinstance(c, list):
            __create_token_subhierarchy(token_hierarchy, c, indentation + "    ")
        else:
            class_name = c[0].__name__
            if class_name not in ("object", "ABC", "module"):
                abstract = " (abstract)" if inspect.isabstract(c[0]) else ""
                line = (
                    f"{indentation[4:]}* "
                    f":py:class:`note_splitter.tokens.{class_name}`{abstract}"
                )
                token_hierarchy.append(line)


save_token_hierarchy()

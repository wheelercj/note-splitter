# how to maintain this documentation

## auto-generating documentation
Each time a new Python module is added to the project:
1. Add its name to the list in docs/modules.rst.
2. Use this command to automatically generate an rst file for the new module: `sphinx-apidoc -o docs note-splitter` (while in the project's root folder).

## custom documentation
We can add custom documentation pages any time in either markdown or [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html). Just put the files in the docs folder and add the file's name to the list in docs/modules.rst. Internal links are simple to add, e.g. for markdown, `[our documentation's homepage](index.rst)` becomes [our documentation's homepage](index.rst). The auto-generated links to a custom file will have the display text of the file's first header, not the file's name (if they're different).

## local testing
We can generate HTML files locally to test the md and rst files. If you haven't already, install Sphinx with `pip install -U Sphinx`.
1. Add the myst_parser extension to the extensions list in docs/conf.py (this is needed to process our markdown files).
2. Use the `make html` command (or if that doesn't work, try `.\make html`) while in the note-splitter/docs folder to generate HTML files from our rst and md files. This is just for testing changes to the rst and md files before committing them; the HTML files should not be committed.
3. Remove the myst_parser extension from the extensions list in docs/conf.py before committing, or the remote documentation build will fail.

## see also
* [Auto-Documenting a Python Project Using Sphinx](https://betterprogramming.pub/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9)

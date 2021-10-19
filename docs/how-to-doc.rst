==================================
how to maintain this documentation
==================================

auto-generating documentation
-----------------------------
Each time a new Python module is added to the project:
 1. Add its name to the list in docs/modules.rst
 2. Use this command to automatically generate an rst file for the new module: :code:`sphinx-apidoc -o docs note-splitter` (while in the project's root folder)

Each time a new third-party library is added to our project:
 1. Add its name (the one used in the :code:`pip install` statement) to the list in docs/environment.yaml

custom documentation
--------------------
We can add custom `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ documentation files. Just put the files in the docs folder and add the file's name to the list in docs/index.rst. `Here's <http://rst.ninjs.org/#>`_ a reStructuredText renderer for previewing the rst files. Read The Docs says they support markdown files, but the only markdown parser they support is no longer maintained and doesn't parse markdown correctly anymore.

local testing
-------------
We can generate HTML files locally to test the rst files. If you haven't already, install Sphinx with :code:`pip install -U Sphinx`.

1. While in the project's root folder, use :code:`cd docs`.
2. Use the :code:`make html` command (or if that doesn't work, try :code:`.\make html`) to generate HTML files from our rst files. This is just for testing changes to the rst files before committing them; the HTML files should not be committed.

see also
--------
* `Auto-Documenting a Python Project Using Sphinx <https://betterprogramming.pub/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9>`_

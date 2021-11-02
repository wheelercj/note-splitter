==================================
how to maintain this documentation
==================================

auto-generating documentation
-----------------------------
Much of our documentation on Read The Docs is automatically built from the code we write (docstrings, typehints, classes, etc.) whenever we commit to the master branch. Sometimes we will need to make small changes to the documentation files to help this automatic documentation continue.

Each time a new Python module is added to the project:
 1. Add its name to the list in docs/modules.rst
 2. Use this command to automatically generate an rst file for the new module: :code:`sphinx-apidoc -o docs note_splitter` (while in the project's root folder)

Each time a new third-party library is added to our project:
 1. Add its name (the one used in the :code:`pip install` statement) to the list in docs/environment.yaml

If a new token type is created and/or the inheritance between token types changes:
 1. Run scripts/token_hierarchy.py to automatically update the docs/token_hierarchy.rst file

custom documentation
--------------------
We can also add our own manually written documentation files. Read The Docs supports both markdown (`MyST's version <https://myst-parser.readthedocs.io/en/latest/>`_) and `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ files. Just put the files in the docs folder and add the file's name to the list in docs/index.rst. `Here's <http://rst.ninjs.org/#>`_ a reStructuredText renderer for previewing rst files.

| Internal links are easy to add.  

Markdown example::

    [file title here](file-name.rst)

reStructuredText example::
    
    `file title here <file-name.html>`_

Note that while a link to a local file in a markdown file can use the :code:`.rst` and :code:`.md` extensions, a link to a local file in an rst file must use the :code:`.html` extension.

local testing
-------------
We can generate HTML files locally to test our rst and markdown files. If you haven't already, install Sphinx with :code:`pip install -U Sphinx`, MyST with :code:`pip install -U myst-parser` and our site's theme with ``pip install sphinx-rtd-theme``.

1. While in the project's root folder, use :code:`cd docs`.
2. Use the :code:`make html` command (or if that doesn't work, try :code:`.\make html`) to generate HTML files from our rst and markdown files. This is just for testing changes to the rst and markdown files before committing them; the HTML files should not be committed.

see also
--------
* `notes on setting up documentation on Read The Docs <doc-setup.html>`_

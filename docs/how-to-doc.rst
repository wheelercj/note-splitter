==================================
how to maintain this documentation
==================================

.. image:: https://readthedocs.org/projects/note-splitter/badge/?version=latest
    :target: https://note-splitter.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

auto-generating documentation
-----------------------------
Much of our documentation on Read The Docs is automatically built from the code we write (docstrings, typehints, classes, etc.) whenever we commit to the master branch. Sometimes we will need to make small changes to the documentation files to help this automatic documentation continue.

Each time a new Python module is added to the project:
 1. Add its name to the list in docs/modules.rst
 2. Use this command to automatically generate an rst file for the new module: ``sphinx-apidoc -o docs src/note_splitter -e`` (while in the project's root folder)

Each time a new dependency is added to our project:
 1. See `dependencies <https://note-splitter.readthedocs.io/en/latest/dev-setup.html#dependencies>`_

custom documentation
--------------------
We can also add our own manually written documentation files. Read The Docs supports both markdown (`MyST's version <https://myst-parser.readthedocs.io/en/latest/>`_) and `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ (rst) files. Just put the files in the docs folder and add the file's name to the list in docs/index.rst. `Here's <http://rst.ninjs.org/#>`_ a reStructuredText renderer for previewing rst files.

| Internal links are easy to add.  

Markdown example:

.. code-block::

  [file title here](file-name.rst)

reStructuredText example:

.. code-block:: rst
  
  `file title here <file-name.html>`_

Note that while a link to a local file in a markdown file can use the ``.rst`` and ``.md`` extensions, a link to a local file in an rst file must use the ``.html`` extension.

local testing
-------------
We can generate HTML files locally to test our rst and markdown files.

1. While in the project's root folder, use ``cd docs``.
2. Use the ``make html`` command (or if that doesn't work, try ``.\make html``) to generate HTML files from our rst and markdown files. This is just for testing changes to the rst and markdown files before committing them; the HTML files should not be committed.

see also
--------
* `notes on setting up documentation on Read The Docs <doc-setup.html>`_

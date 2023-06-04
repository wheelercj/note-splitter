==================================
how to maintain this documentation
==================================

You can see `the documentation build status here <https://readthedocs.org/projects/note-splitter/builds/>`_. Click on a build for more details.

Most of the documentation is automatically generated directly from the code and docstrings whenever commit(s) are added to the main branch on GitHub, but sometimes manual changes are needed as explained in [maintenance](https://github.com/wheelercj/note-splitter/blob/main/docs/dev-setup.md#maintenance).

We can also add our own custom documentation files. Read The Docs supports both markdown (`MyST's version <https://myst-parser.readthedocs.io/en/latest/>`_) and `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ (rst) files. Just put the files in the docs folder and add the file's name to the list in docs/index.rst. `Here's <http://rst.ninjs.org/#>`_ a reStructuredText renderer for previewing rst files.

| Internal links are easy to add.

Markdown example:

.. code-block::

  [file title here](file-name.rst)

reStructuredText example:

.. code-block:: rst

  `file title here <file-name.html>`_

Note that while links to local files in a markdown file can use the ``.rst`` and ``.md`` extensions, a link to a local file in an rst file must use the ``.html`` extension.

local testing
-------------
We can generate HTML files locally to test our rst and markdown files.

1. While in the project's root folder, use ``cd docs``.
2. Use the ``make html`` command (or if that doesn't work, try ``.\make html``) to generate HTML files from our rst and markdown files. This is just for testing changes to the rst and markdown files before committing them; the HTML files should not be committed.

see also
--------
* `notes on setting up documentation on Read The Docs <doc-setup.html>`_

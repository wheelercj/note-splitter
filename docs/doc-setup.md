# notes on setting up documentation on Read The Docs

If you get stuck on one of these steps, there are some cases where it might be helpful to come back to the step later.

1. Make the project a local package. [Real Python's guide](https://realpython.com/python-import/#create-and-install-a-local-package) and [mCoding's video on project structure](https://youtu.be/DhUpxWjOhME?t=176) might help. Be sure to install the package locally (using `pip install -e .`).
2. Go through the [Read The Docs tutorial](https://docs.readthedocs.io/en/stable/tutorial/).
3. Go through the Read The Docs guide to [Getting Started with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html). More details on what to do with conf.py [here](https://betterprogramming.pub/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9) and [here](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html). Using the myst_parser extension is fine when running Sphinx commands locally, but remove the extension from the extensions list before having Read The Docs run them to prevent problems.
4. You might want to go through some other Read The Docs guides such as [how to make a configuration file](https://docs.readthedocs.io/en/stable/config-file/index.html), or the [Sphinx step-by-step guide](https://docs.readthedocs.io/en/stable/guides/tools.html).
5. Set up the project to use Sphinx, and make sure it was done correctly by trying the sphinx commands.
6. The other guides here don't mention that you need to add `myst-parser` to your list of installs in environment.yaml (see example below).
7. Create a Read The Docs account if you don't have one already, and link it to the GitHub account that owns the repo that needs the documentation.
8. Go through the [Read The Docs tutorial](https://docs.readthedocs.io/en/stable/tutorial/) again, but this time for your own project.

## example environment.yaml

```
name: docs
channels:
  - conda-forge
  - defaults
dependencies:
  - sphinx==4.2.0
  - pip
  - myst-parser
  - pyyaml
```

## see also

* [how to maintain this documentation](how-to-doc.rst)

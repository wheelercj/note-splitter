# development environment

## setup

1. Download [Python](https://www.python.org/downloads/) 3.11 if you haven't already.
2. Navigate in a terminal to where you want the project's folder to appear.
3. `git clone https://github.com/wheelercj/note-splitter.git` to download the project's files.
4. `cd` into the project's folder.
5. Create a virtual environment, such as with `py -3.11 -m venv venv` or `python3.11 -m venv venv`.
6. [Activate the virtual environment](https://python.land/virtual-environments/virtualenv).
7. `pip install -r requirements.txt` to install the app's dependencies.
8. `pip install -r requirements-dev.txt` to install the development dependencies.
9. `pre-commit install` to set up [pre-commit](https://pre-commit.com/) git hook scripts.

Now you can use these commands:

* `briefcase dev` to run the app in dev mode (see [BeeWare Briefcase's docs](https://docs.beeware.org/en/latest/tutorial/tutorial-3.html) for more info if needed).
* `pytest` to run the automated tests.
* `py src/tests/manual_test.py` or `python3 src/tests/manual_test.py` to run the manual test.
* `coverage run -m pytest` to gather test coverage data, and then:
  * `coverage report -i` to view a brief test coverage report.
  * `coverage html -i` to view a detailed test coverage report.
* `pre-commit run --all-files` to run all the pre-commit hooks without committing.
* `pre-commit run hook-id-here --file file-path-here.py` to run one pre-commit hook on one file without committing.
* To locally build the documentation to test it, see [how to maintain this documentation](how-to-doc.rst).

## maintenance

* when the dependencies change
  * update the appropriate requirements file
  * if the new dependency is for Note Splitter itself and not just a development dependency, add it to docs/environment.yaml
* when a new Python module is added
  * add its name to the list in docs/modules.rst
  * while in the project’s root folder, use this command to automatically generate an rst file for the new module: `sphinx-apidoc -o docs src/note_splitter -e`
* when bumping the app's version: search the entire project for the version to change because it is in multiple places

## distribution

* `briefcase dev` to run the app in dev mode.
* `briefcase create` to create the app template.
* `briefcase update` to copy new changes into the platform directory.
* `briefcase update -d` to update the dependencies in the packaged app.
* `briefcase build` to compile the app.
* `briefcase run` to run the compiled app.
* `briefcase run -u` to update, build, and run the compiled app.
* `briefcase package` to create the app's installer for the current platform.
* `briefcase package -u` to update, build, and create the app's installer for the current platform.

## directory structure

Here are descriptions of what each of Note Splitter's folders are for:

```
.
├───.github             # Files to configure GitHub.
│   ├── ISSUE_TEMPLATE  # Issue templates.
│   └── workflows       # GitHub Actions configuration files for automated testing.
├── docs                # Files for documentation (.md and .rst) and for configuration.
│   └── images          # Images used in the documentation and/or the README.
└── src
    ├── note_splitter   # Note Splitter's source code.
    │   └── resources   # Note Splitter's icon files.
    └── tests           # Automated and manual tests.
        └── assets      # Files used by automated and manual tests.
```

## further reading

You can learn more about how this program was made from our [references](references.md).

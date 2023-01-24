from textwrap import dedent

from PySide6 import QtWidgets


class AboutTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(
            QtWidgets.QLabel(
                dedent(
                    """\
                    <p><h1>Note Splitter</h1> v0.0.1</p>

                    <p>Split markdown files into multiple smaller files.</p>

                    <ul>
                        <li><a href="%(url)s/blob/main/README.md">instructions</a></li>
                        <li><a href="%(url)s/blob/main/LICENSE">license</a></li>
                        <li><a href="%(url)s/discussions">join the discussion</a></li>
                        <li><a href="%(url)s/issues">report a bug or request a feature</a></li>
                        <li><a href="%(url)s">source code</a></li>
                    </ul>
                    """  # noqa: E501
                    % {"url": "https://github.com/wheelercj/note-splitter"}
                )
            )
        )

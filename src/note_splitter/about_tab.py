from textwrap import dedent

from PySide6 import QtWidgets


class AboutTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        label = QtWidgets.QLabel(
            dedent(
                """\
                <style>
                    h1 {
                        font-size: 1.4em;
                        font-weight: bold;
                    }
                    p {
                        font-size: 1.2em;
                    }
                    ul {
                        font-size: 1.2em;
                        padding-left: 0;
                    }
                    li {
                        margin-bottom: 0.5em;
                    }
                    a {
                        color: #89d3ff;
                    }
                </style>

                <h1>Note Splitter</h1>
                <p style="font-size: 0.8em">v1.0.0</p>

                <p>Split markdown files into multiple smaller files.</p>

                <ul>
                    <li><a href="%(url)s/blob/main/README.md">instructions</a></li>
                    <li><a href="%(url)s/releases">check for updates</a></li>
                    <li><a href="%(url)s/blob/main/LICENSE">license</a></li>
                    <li><a href="%(url)s/discussions">join the discussion</a></li>
                    <li><a href="%(url)s/issues">report a bug or request a feature</a></li>
                    <li><a href="%(url)s">source code</a></li>
                </ul>

                <p>App icon provided by <a href="https://icons8.com">Icons8</a>.</p>
                """  # noqa: E501
                % {"url": "https://github.com/wheelercj/note-splitter"}
            )
        )
        label.setOpenExternalLinks(True)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(label)
        self.layout.addStretch()

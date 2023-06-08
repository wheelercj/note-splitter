from textwrap import dedent

from note_splitter.settings import DEFAULT_SETTINGS
from note_splitter.settings import update_from_line_edit
from PySide6 import QtCore
from PySide6 import QtWidgets


class PatternsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)
        label = QtWidgets.QLabel(
            dedent(
                """\
                <style>
                    a {
                        color: #89d3ff;
                    }
                </style>
                <p>These are the regular expressions used to identify the various
                elements of a <br> note. You will probably never need to change them,
                but if you do and you <br> don't know how, feel free to join the
                <a href="%(url)s/discussions">discussions</a> or make an
                <a href="%(url)s/issues">issue</a> on GitHub.</p>
                """
                % {"url": "https://github.com/wheelercj/note-splitter"}
            )
        )
        label.setOpenExternalLinks(True)
        self.layout.addWidget(label)
        settings = QtCore.QSettings()
        self.blockquote_line_edit = QtWidgets.QLineEdit(
            settings.value("blockquote_pattern", DEFAULT_SETTINGS["blockquote_pattern"])
        )
        self.blockquote_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "blockquote_pattern", self.blockquote_line_edit
            )
        )
        self.layout.addRow("blockquote (full-line):", self.blockquote_line_edit)
        self.code_fence_line_edit = QtWidgets.QLineEdit(
            settings.value("code_fence_pattern", DEFAULT_SETTINGS["code_fence_pattern"])
        )
        self.code_fence_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "code_fence_pattern", self.code_fence_line_edit
            )
        )
        self.layout.addRow("code fence (full-line):", self.code_fence_line_edit)
        self.empty_line_line_edit = QtWidgets.QLineEdit(
            settings.value("empty_line_pattern", DEFAULT_SETTINGS["empty_line_pattern"])
        )
        self.empty_line_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "empty_line_pattern", self.empty_line_line_edit
            )
        )
        self.layout.addRow("empty line (full-line):", self.empty_line_line_edit)
        self.file_path_in_link_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "file_path_in_link_pattern",
                DEFAULT_SETTINGS["file_path_in_link_pattern"],
            )
        )
        self.file_path_in_link_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "file_path_in_link_pattern", self.file_path_in_link_line_edit
            )
        )
        self.layout.addRow(
            "file path in link (inline):", self.file_path_in_link_line_edit
        )
        self.finished_task_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "finished_task_pattern", DEFAULT_SETTINGS["finished_task_pattern"]
            )
        )
        self.finished_task_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "finished_task_pattern", self.finished_task_line_edit
            )
        )
        self.layout.addRow("finished task (full-line):", self.finished_task_line_edit)
        self.footnote_line_edit = QtWidgets.QLineEdit(
            settings.value("footnote_pattern", DEFAULT_SETTINGS["footnote_pattern"])
        )
        self.footnote_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("footnote_pattern", self.footnote_line_edit)
        )
        self.layout.addRow("footnote (full-line):", self.footnote_line_edit)
        self.frontmatter_fence_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "frontmatter_fence_pattern",
                DEFAULT_SETTINGS["frontmatter_fence_pattern"],
            )
        )
        self.frontmatter_fence_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "frontmatter_fence_pattern", self.frontmatter_fence_line_edit
            )
        )
        self.layout.addRow(
            "frontmatter fence (full-line):", self.frontmatter_fence_line_edit
        )
        self.header_line_edit = QtWidgets.QLineEdit(
            settings.value("header_pattern", DEFAULT_SETTINGS["header_pattern"])
        )
        self.header_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("header_pattern", self.header_line_edit)
        )
        self.layout.addRow("header (full-line):", self.header_line_edit)
        self.horizontal_rule_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "horizontal_rule_pattern", DEFAULT_SETTINGS["horizontal_rule_pattern"]
            )
        )
        self.horizontal_rule_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "horizontal_rule_pattern", self.horizontal_rule_line_edit
            )
        )
        self.layout.addRow(
            "horizontal rule (full-line):", self.horizontal_rule_line_edit
        )
        self.math_fence_line_edit = QtWidgets.QLineEdit(
            settings.value("math_fence_pattern", DEFAULT_SETTINGS["math_fence_pattern"])
        )
        self.math_fence_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "math_fence_pattern", self.math_fence_line_edit
            )
        )
        self.layout.addRow("math fence (full-line):", self.math_fence_line_edit)
        self.ordered_list_item_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "ordered_list_item_pattern",
                DEFAULT_SETTINGS["ordered_list_item_pattern"],
            )
        )
        self.ordered_list_item_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "ordered_list_item_pattern", self.ordered_list_item_line_edit
            )
        )
        self.layout.addRow(
            "ordered list item (full-line):", self.ordered_list_item_line_edit
        )
        self.table_divider_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "table_divider_pattern", DEFAULT_SETTINGS["table_divider_pattern"]
            )
        )
        self.table_divider_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "table_divider_pattern", self.table_divider_line_edit
            )
        )
        self.layout.addRow("table divider (full-line):", self.table_divider_line_edit)
        self.table_row_line_edit = QtWidgets.QLineEdit(
            settings.value("table_row_pattern", DEFAULT_SETTINGS["table_row_pattern"])
        )
        self.table_row_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("table_row_pattern", self.table_row_line_edit)
        )
        self.layout.addRow("table row (full-line):", self.table_row_line_edit)
        self.tag_line_edit = QtWidgets.QLineEdit(
            settings.value("tag_pattern", DEFAULT_SETTINGS["tag_pattern"])
        )
        self.tag_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("tag_pattern", self.tag_line_edit)
        )
        self.layout.addRow("tag (inline):", self.tag_line_edit)
        self.task_line_edit = QtWidgets.QLineEdit(
            settings.value("task_pattern", DEFAULT_SETTINGS["task_pattern"])
        )
        self.task_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("task_pattern", self.task_line_edit)
        )
        self.layout.addRow("task (full-line):", self.task_line_edit)
        self.unordered_list_item_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "unordered_list_item_pattern",
                DEFAULT_SETTINGS["unordered_list_item_pattern"],
            )
        )
        self.unordered_list_item_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "unordered_list_item_pattern", self.unordered_list_item_line_edit
            )
        )
        self.layout.addRow(
            "unordered list item (full-line):", self.unordered_list_item_line_edit
        )

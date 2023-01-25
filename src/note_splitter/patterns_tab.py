from note_splitter.settings import update_from_le
from PySide6 import QtWidgets


class PatternsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)
        self.blockquote_line_edit = QtWidgets.QLineEdit()
        self.blockquote_line_edit.editingFinished.connect(
            lambda le=self.blockquote_line_edit: update_from_le(
                "blockquote_pattern", le
            )
        )
        self.layout.addRow("blockquote (full-line):", self.blockquote_line_edit)
        self.code_fence_line_edit = QtWidgets.QLineEdit()
        self.code_fence_line_edit.editingFinished.connect(
            lambda le=self.code_fence_line_edit: update_from_le(
                "code_fence_pattern", le
            )
        )
        self.layout.addRow("code fence (full-line):", self.code_fence_line_edit)
        self.empty_line_line_edit = QtWidgets.QLineEdit()
        self.empty_line_line_edit.editingFinished.connect(
            lambda le=self.empty_line_line_edit: update_from_le(
                "empty_line_pattern", le
            )
        )
        self.layout.addRow("empty line (full-line):", self.empty_line_line_edit)
        self.file_path_in_link_line_edit = QtWidgets.QLineEdit()
        self.file_path_in_link_line_edit.editingFinished.connect(
            lambda le=self.file_path_in_link_line_edit: update_from_le(
                "file_path_in_link_pattern", le
            )
        )
        self.layout.addRow(
            "file path in link (inline):", self.file_path_in_link_line_edit
        )
        self.finished_task_line_edit = QtWidgets.QLineEdit()
        self.finished_task_line_edit.editingFinished.connect(
            lambda le=self.finished_task_line_edit: update_from_le(
                "finished_task_pattern", le
            )
        )
        self.layout.addRow("finished task (full-line):", self.finished_task_line_edit)
        self.footnote_line_edit = QtWidgets.QLineEdit()
        self.footnote_line_edit.editingFinished.connect(
            lambda le=self.footnote_line_edit: update_from_le("footnote_pattern", le)
        )
        self.layout.addRow("footnote (full-line):", self.footnote_line_edit)
        self.frontmatter_fence_line_edit = QtWidgets.QLineEdit()
        self.frontmatter_fence_line_edit.editingFinished.connect(
            lambda le=self.frontmatter_fence_line_edit: update_from_le(
                "frontmatter_fence_pattern", le
            )
        )
        self.layout.addRow(
            "frontmatter fence (full-line):", self.frontmatter_fence_line_edit
        )
        self.header_line_edit = QtWidgets.QLineEdit()
        self.header_line_edit.editingFinished.connect(
            lambda le=self.header_line_edit: update_from_le("header_pattern", le)
        )
        self.layout.addRow("header (full-line):", self.header_line_edit)
        self.horizontal_rule_line_edit = QtWidgets.QLineEdit()
        self.horizontal_rule_line_edit.editingFinished.connect(
            lambda le=self.horizontal_rule_line_edit: update_from_le(
                "horizontal_rule_pattern", le
            )
        )
        self.layout.addRow(
            "horizontal rule (full-line):", self.horizontal_rule_line_edit
        )
        self.math_fence_line_edit = QtWidgets.QLineEdit()
        self.math_fence_line_edit.editingFinished.connect(
            lambda le=self.math_fence_line_edit: update_from_le(
                "math_fence_pattern", le
            )
        )
        self.layout.addRow("math fence (full-line):", self.math_fence_line_edit)
        self.ordered_list_item_line_edit = QtWidgets.QLineEdit()
        self.ordered_list_item_line_edit.editingFinished.connect(
            lambda le=self.ordered_list_item_line_edit: update_from_le(
                "ordered_list_item_pattern", le
            )
        )
        self.layout.addRow(
            "ordered list item (full-line):", self.ordered_list_item_line_edit
        )
        self.table_divider_line_edit = QtWidgets.QLineEdit()
        self.table_divider_line_edit.editingFinished.connect(
            lambda le=self.table_divider_line_edit: update_from_le(
                "table_divider_pattern", le
            )
        )
        self.layout.addRow("table divider (full-line):", self.table_divider_line_edit)
        self.table_row_line_edit = QtWidgets.QLineEdit()
        self.table_row_line_edit.editingFinished.connect(
            lambda le=self.table_row_line_edit: update_from_le("table_row_pattern", le)
        )
        self.layout.addRow("table row (full-line):", self.table_row_line_edit)
        self.tag_line_edit = QtWidgets.QLineEdit()
        self.tag_line_edit.editingFinished.connect(
            lambda le=self.tag_line_edit: update_from_le("tag_pattern", le)
        )
        self.layout.addRow("tag (inline):", self.tag_line_edit)
        self.task_line_edit = QtWidgets.QLineEdit()
        self.task_line_edit.editingFinished.connect(
            lambda le=self.task_line_edit: update_from_le("task_pattern", le)
        )
        self.layout.addRow("task (full-line):", self.task_line_edit)
        self.unordered_list_item_line_edit = QtWidgets.QLineEdit()
        self.unordered_list_item_line_edit.editingFinished.connect(
            lambda le=self.unordered_list_item_line_edit: update_from_le(  # noqa: E501
                "unordered_list_item_pattern", le
            )
        )
        self.layout.addRow(
            "unordered list item (full-line):", self.unordered_list_item_line_edit
        )

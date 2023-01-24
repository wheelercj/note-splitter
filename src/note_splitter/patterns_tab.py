from PySide6 import QtWidgets


class PatternsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)
        self.blockquote_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("blockquote (full-line):", self.blockquote_line_edit)
        self.code_fence_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("code fence (full-line):", self.code_fence_line_edit)
        self.empty_line_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("empty line (full-line):", self.empty_line_line_edit)
        self.file_path_in_link_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow(
            "file path in link (inline):", self.file_path_in_link_line_edit
        )
        self.finished_task_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("finished task (full-line):", self.finished_task_line_edit)
        self.footnote_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("footnote (full-line):", self.footnote_line_edit)
        self.frontmatter_fence_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow(
            "frontmatter fence (full-line):", self.frontmatter_fence_line_edit
        )
        self.header_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("header (full-line):", self.header_line_edit)
        self.horizontal_rule_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow(
            "horizontal rule (full-line):", self.horizontal_rule_line_edit
        )
        self.math_fence_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("math fence (full-line):", self.math_fence_line_edit)
        self.ordered_list_item_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow(
            "ordered list item (full-line):", self.ordered_list_item_line_edit
        )
        self.table_divider_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("table divider (full-line):", self.table_divider_line_edit)
        self.table_row_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("table row (full-line):", self.table_row_line_edit)
        self.tag_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("tag (inline):", self.tag_line_edit)
        self.task_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow("task (full-line):", self.task_line_edit)
        self.unordered_list_item_line_edit = QtWidgets.QLineEdit()
        self.layout.addRow(
            "unordered list item (full-line):", self.unordered_list_item_line_edit
        )

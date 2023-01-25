from note_splitter.gui import folder_browse
from note_splitter.settings import update_from_checkbox
from note_splitter.settings import update_from_le
from PySide6 import QtWidgets


class SettingsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.source_folder_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.source_folder_layout)
        self.source_folder_layout.addWidget(QtWidgets.QLabel("source folder:"))
        self.source_folder_line_edit = QtWidgets.QLineEdit()
        self.source_folder_line_edit.editingFinished.connect(
            lambda le=self.source_folder_line_edit: update_from_le(
                "source_folder_path", le
            )
        )
        self.source_folder_layout.addWidget(self.source_folder_line_edit)
        self.source_folder_browse_button = QtWidgets.QPushButton("browse")
        self.source_folder_browse_button.clicked.connect(
            lambda self=self: folder_browse(
                self.source_folder_line_edit,
                "choose the source folder",
            )
        )
        self.source_folder_layout.addWidget(self.source_folder_browse_button)
        self.source_folder_layout.addStretch()

        self.destination_folder_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.destination_folder_layout)
        self.destination_folder_layout.addWidget(
            QtWidgets.QLabel("destination folder:")
        )
        self.destination_folder_line_edit = QtWidgets.QLineEdit()
        self.destination_folder_line_edit.editingFinished.connect(
            lambda le=self.destination_folder_line_edit: update_from_le(
                "destination_folder_path", le
            )
        )
        self.destination_folder_layout.addWidget(self.destination_folder_line_edit)
        self.destination_folder_browse_button = QtWidgets.QPushButton("browse")
        self.destination_folder_browse_button.clicked.connect(
            lambda self=self: folder_browse(
                self.destination_folder_line_edit,
                "choose the destination folder",
            )
        )
        self.destination_folder_layout.addWidget(self.destination_folder_browse_button)
        self.destination_folder_layout.addStretch()

        self.file_name_format_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.file_name_format_layout)
        self.file_name_format_layout.addWidget(
            QtWidgets.QLabel("new file name format:")
        )
        self.new_file_name_format_line_edit = QtWidgets.QLineEdit()
        self.new_file_name_format_line_edit.editingFinished.connect(
            lambda le=self.new_file_name_format_line_edit: update_from_le(
                "file_name_format", le
            )
        )
        self.file_name_format_layout.addWidget(self.new_file_name_format_line_edit)
        self.file_name_format_layout.addStretch()

        self.checkboxes_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(self.checkboxes_layout)
        self.create_index_file_checkbox = QtWidgets.QCheckBox()
        self.create_index_file_checkbox.stateChanged.connect(
            lambda cb=self.create_index_file_checkbox: update_from_checkbox(
                "create_index_file", cb
            )
        )
        self.checkboxes_layout.addRow(
            "create index file:", self.create_index_file_checkbox
        )
        self.create_index_file_checkbox.setChecked(True)
        self.remove_split_keyword_checkbox = QtWidgets.QCheckBox()
        self.remove_split_keyword_checkbox.stateChanged.connect(
            lambda cb=self.remove_split_keyword_checkbox: update_from_checkbox(
                "remove_split_keyword", cb
            )
        )
        self.checkboxes_layout.addRow(
            "remove split keyword:", self.remove_split_keyword_checkbox
        )
        self.remove_split_keyword_checkbox.setChecked(True)
        self.move_footnotes_checkbox = QtWidgets.QCheckBox()
        self.move_footnotes_checkbox.stateChanged.connect(
            lambda cb=self.move_footnotes_checkbox: update_from_checkbox(
                "move_footnotes", cb
            )
        )
        self.checkboxes_layout.addRow("move footnotes:", self.move_footnotes_checkbox)
        self.move_footnotes_checkbox.setChecked(True)
        self.copy_frontmatter_checkbox = QtWidgets.QCheckBox()
        self.copy_frontmatter_checkbox.stateChanged.connect(
            lambda cb=self.copy_frontmatter_checkbox: update_from_checkbox(
                "copy_frontmatter", cb
            )
        )
        self.checkboxes_layout.addRow(
            "copy frontmatter:", self.copy_frontmatter_checkbox
        )
        self.copy_frontmatter_checkbox.setChecked(False)
        self.copy_global_tags_checkbox = QtWidgets.QCheckBox()
        self.copy_global_tags_checkbox.stateChanged.connect(
            lambda cb=self.copy_global_tags_checkbox: update_from_checkbox(
                "copy_global_tags", cb
            )
        )
        self.checkboxes_layout.addRow(
            "copy global tags:", self.copy_global_tags_checkbox
        )
        self.copy_global_tags_checkbox.setChecked(True)
        self.create_backlinks_checkbox = QtWidgets.QCheckBox()
        self.create_backlinks_checkbox.stateChanged.connect(
            lambda cb=self.create_backlinks_checkbox: update_from_checkbox(
                "create_backlinks", cb
            )
        )
        self.checkboxes_layout.addRow(
            "create backlinks:", self.create_backlinks_checkbox
        )
        self.create_backlinks_checkbox.setChecked(False)

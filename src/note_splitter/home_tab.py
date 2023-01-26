from note_splitter.gui import files_browse
from note_splitter.settings import update_from_checkbox
from note_splitter.settings import update_from_combo_box
from note_splitter.settings import update_from_le
from PySide6 import QtWidgets


class HomeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("Choose files to split:"))
        files_choosing_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(files_choosing_layout)
        self.browse_button = QtWidgets.QPushButton("browse")
        files_choosing_layout.addWidget(self.browse_button)
        files_choosing_layout.addWidget(QtWidgets.QLabel(" or "))
        self.search_button = QtWidgets.QPushButton("search")
        self.search_button.clicked.connect(
            # TODO
        )
        files_choosing_layout.addWidget(self.search_button)
        self.keyword_line_edit = QtWidgets.QLineEdit()
        self.keyword_line_edit.editingFinished.connect(
            lambda le=self.keyword_line_edit: update_from_le("split_keyword", le)
        )
        files_choosing_layout.addWidget(self.keyword_line_edit)

        self.layout.addWidget(QtWidgets.QLabel("Files to split:"))
        self.file_list_text_browser = QtWidgets.QTextBrowser()
        self.abs_paths_of_files_to_split: list[str] = []
        self.browse_button.clicked.connect(lambda: self.__get_files_to_split())
        self.layout.addWidget(self.file_list_text_browser)

        self.layout.addWidget(QtWidgets.QLabel("Choose what to split by:"))
        self.split_by_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.split_by_layout)
        self.type_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.type_layout)
        self.type_layout.addWidget(QtWidgets.QLabel("type:"))
        self.type_combo_box = QtWidgets.QComboBox()
        self.type_combo_box.currentTextChanged.connect(
            lambda cb=self.type_combo_box: update_from_combo_box("split_type", cb)
        )
        self.type_layout.addWidget(self.type_combo_box)
        self.attribute_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.attribute_layout)
        self.attribute_layout.addWidget(QtWidgets.QLabel("attribute:"))
        self.attribute_combo_box = QtWidgets.QComboBox()
        self.attribute_combo_box.currentTextChanged.connect(
            lambda cb=self.attribute_combo_box: update_from_combo_box("split_attrs", cb)
        )
        self.attribute_layout.addWidget(self.attribute_combo_box)
        self.value_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.value_layout)
        self.value_layout.addWidget(QtWidgets.QLabel("value:"))
        self.value_line_edit = QtWidgets.QLineEdit()
        self.value_line_edit.textChanged.connect(
            lambda le=self.value_line_edit: update_from_le("split_value", le)
        )
        self.value_layout.addWidget(self.value_line_edit)

        self.parse_blocks_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.parse_blocks_layout)
        self.parse_blocks_checkbox = QtWidgets.QCheckBox()
        self.parse_blocks_checkbox.changeEvent.connect(
            lambda cb=self.parse_blocks_checkbox: update_from_checkbox(
                "parse_blocks", cb
            )
        )
        self.parse_blocks_layout.addWidget(self.parse_blocks_checkbox)
        self.parse_blocks_layout.addWidget(QtWidgets.QLabel("parse blocks"))
        self.parse_blocks_layout.addStretch()

        self.split_buttons_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.split_buttons_layout)
        self.split_all_button = QtWidgets.QPushButton("split all")
        self.split_all_button.clicked.connect(
            # TODO
        )
        self.split_buttons_layout.addWidget(self.split_all_button)
        self.split_selected_button = QtWidgets.QPushButton("split selected")
        self.split_selected_button.clicked.connect(
            # TODO
        )
        self.split_buttons_layout.addWidget(self.split_selected_button)
        self.split_buttons_layout.addStretch()

    def __get_files_to_split(self) -> None:
        self.abs_paths_of_files_to_split = files_browse(
            self, self.file_list_text_browser, "choose files to split"
        )

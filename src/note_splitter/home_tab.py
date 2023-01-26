import inspect

from note_splitter import tokens
from note_splitter.gui import files_browse
from note_splitter.settings import get_token_type
from note_splitter.settings import get_token_type_names
from note_splitter.settings import update_from_checkbox
from note_splitter.settings import update_from_combo_box
from note_splitter.settings import update_from_line_edit
from PySide6 import QtCore
from PySide6 import QtWidgets


class HomeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        settings = QtCore.QSettings()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("Choose files to split:"))
        files_choosing_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(files_choosing_layout)
        self.browse_button = QtWidgets.QPushButton("browse")
        files_choosing_layout.addWidget(self.browse_button)
        files_choosing_layout.addWidget(QtWidgets.QLabel(" or "))
        self.keyword_search_button = QtWidgets.QPushButton("search by keyword")
        self.keyword_search_button.clicked.connect(
            # TODO
        )
        files_choosing_layout.addWidget(self.keyword_search_button)
        self.keyword_line_edit = QtWidgets.QLineEdit(settings.value("split_keyword"))
        self.keyword_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("split_keyword", self.keyword_line_edit)
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
        token_type_names = get_token_type_names()
        token_type_names.remove("section")
        self.type_combo_box.addItems(token_type_names)
        self.type_combo_box.setCurrentText(settings.value("split_type"))
        self.type_combo_box.currentTextChanged.connect(self.__on_split_type_change)
        self.type_layout.addWidget(self.type_combo_box)
        self.attribute_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.attribute_layout)
        self.attribute_layout.addWidget(QtWidgets.QLabel("attribute:"))
        self.attribute_combo_box = QtWidgets.QComboBox()
        self.attribute_combo_box.addItems(self.__get_split_type_attr_names())
        self.attribute_combo_box.currentTextChanged.connect(self.__on_split_attr_change)
        self.attribute_layout.addWidget(self.attribute_combo_box)
        self.value_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.value_layout)
        self.value_layout.addWidget(QtWidgets.QLabel("value:"))
        self.value_line_edit = QtWidgets.QLineEdit()
        self.value_line_edit.textChanged.connect(
            lambda: update_from_line_edit("split_value", self.value_line_edit)
        )
        self.value_layout.addWidget(self.value_line_edit)

        self.parse_blocks_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.parse_blocks_layout)
        self.parse_blocks_checkbox = QtWidgets.QCheckBox()
        self.parse_blocks_checkbox.changeEvent.connect(
            lambda: update_from_checkbox("parse_blocks", self.parse_blocks_checkbox)
        )
        self.parse_blocks_layout.addWidget(self.parse_blocks_checkbox)
        self.parse_blocks_layout.addWidget(QtWidgets.QLabel("parse blocks"))
        self.parse_blocks_layout.addStretch()

        self.split_button = QtWidgets.QPushButton("split")
        self.split_button.clicked.connect(
            # TODO
        )
        self.layout.addWidget(self.split_button)
        self.layout.addStretch()

    def __on_split_type_change(self) -> None:
        update_from_combo_box("split_type", self.type_combo_box)
        self.attribute_combo_box.clear()
        attr_names: list[str] = self.__get_split_type_attr_names()
        self.attribute_combo_box.addItems(attr_names)
        settings = QtCore.QSettings()
        settings.setValue("split_attrs", {attr_names[0]} if attr_names else {})
        self.value_line_edit.clear()

    def __on_split_attr_change(self) -> None:
        update_from_combo_box("split_attrs", self.attribute_combo_box)
        self.value_line_edit.clear()

    def __get_files_to_split(self) -> None:
        """Shows a file dialog and saves the selected files."""
        self.abs_paths_of_files_to_split = files_browse(
            self, self.file_list_text_browser, "choose files to split"
        )

    def __get_split_type_attr_names(self) -> list[str]:
        """Returns a list of attribute names of the split type."""
        split_type: type[tokens.Token] = get_token_type(
            QtCore.QSettings().value("split_type")
        )
        if inspect.isabstract(split_type):
            attr_names: list[str] = []
        else:
            attr_names = sorted(list(split_type().__dict__.keys()))
            if issubclass(split_type, tokens.Block):
                attr_names.remove("content")
        return attr_names

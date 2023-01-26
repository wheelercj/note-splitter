import inspect
import os

from note_splitter import tokens
from note_splitter.gui import files_browse
from note_splitter.gui import request_folder_path
from note_splitter.gui import show_message
from note_splitter.note import Note
from note_splitter.settings import get_token_type
from note_splitter.settings import get_token_type_names
from note_splitter.settings import update_from_checkbox
from note_splitter.settings import update_from_combo_box
from note_splitter.settings import update_from_line_edit
from PySide6 import QtCore
from PySide6 import QtWidgets


class HomeTab(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.main_window = main_window
        settings = QtCore.QSettings()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("Choose files to split:"))
        files_choosing_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(files_choosing_layout)
        self.browse_button = QtWidgets.QPushButton("browse")
        files_choosing_layout.addWidget(self.browse_button)
        files_choosing_layout.addWidget(QtWidgets.QLabel(" or "))
        self.keyword_search_button = QtWidgets.QPushButton("find by keyword")
        self.keyword_search_button.clicked.connect(self.__on_keyword_search)
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
        self.split_button.clicked.connect(self.__on_split_button_click)
        self.layout.addWidget(self.split_button)
        self.layout.addStretch()

    def __on_keyword_search(self) -> None:
        """Searches for files with the keyword and updates the file list."""
        self.abs_paths_of_files_to_split = []
        keyword = self.keyword_line_edit.text()
        if not keyword:
            show_message("No keyword entered.")
            return
        QtCore.QSettings().setValue("using_split_keyword", True)
        all_notes: list[Note] = self.__get_all_notes()
        if not all_notes:
            return
        chosen_notes = self.__get_chosen_notes(all_notes)
        if not chosen_notes:
            show_message("No notes found.")
            return
        self.file_list_text_browser.setText("\n".join(n.title for n in chosen_notes))

    def __on_split_type_change(self) -> None:
        update_from_combo_box("split_type", self.type_combo_box)
        self.attribute_combo_box.clear()
        attr_names: list[str] = self.__get_split_type_attr_names()
        self.attribute_combo_box.addItems(attr_names)
        QtCore.QSettings().setValue(
            "split_attrs", {attr_names[0]} if attr_names else {}
        )
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

    def __on_split_button_click(self) -> None:
        # TODO
        # new_notes: list[note.Note] = split_files(window, listbox_notes)
        # gui.run_split_summary_window(new_notes, all_notes)
        # window["-NOTES TO SPLIT-"].update(values=[])
        pass

    def __get_all_notes(self) -> list[Note]:
        """Gets all the notes in the user's chosen source folder.

        If a source folder has not been chosen yet, it will ask the user to choose one.
        """
        notes: list[Note] = []
        folder_list: list[str]
        settings = QtCore.QSettings()
        source_folder_path: str | None = settings.value("source_folder_path")
        try:
            folder_list = os.listdir(source_folder_path)
        except FileNotFoundError:
            source_folder_path = request_folder_path("source")
            if not source_folder_path:
                return []
            else:
                settings.setValue("source_folder_path", source_folder_path)
                self.main_window.settings_tab.source_folder_line_edit.setText(
                    source_folder_path
                )
                folder_list = os.listdir(source_folder_path)
        note_types: list[str] = settings.value("note_types")
        assert source_folder_path is not None
        for file_name in folder_list:
            file_path: str = os.path.join(source_folder_path, file_name)
            if os.path.isfile(file_path):
                _, file_ext = os.path.splitext(file_name)
                if file_ext in note_types:
                    notes.append(Note(file_path, source_folder_path, file_name))
        return notes

    def __get_chosen_notes(self, all_notes: list[Note] | None = None) -> list[Note]:
        """Gets the notes that the user chose to split.

        Parameters
        ----------
        all_notes : list[Note], optional
            The list of all the notes in the user's chosen folder. If not provided, the
            list of all the notes in the user's chosen folder will be retrieved.
        """
        if all_notes is None:
            all_notes = self.__get_all_notes()
        if not all_notes:
            return []
        split_keyword: str = QtCore.QSettings().value("split_keyword")
        chosen_notes: list[Note] = []
        for note in all_notes:
            with open(note.path, "r", encoding="utf8") as file:
                contents = file.read()
            if split_keyword in contents:
                chosen_notes.append(note)
        return chosen_notes

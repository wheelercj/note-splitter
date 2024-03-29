import inspect
import os
from typing import Callable

from note_splitter import tokens
from note_splitter.formatter_ import Formatter
from note_splitter.gui import files_browse
from note_splitter.gui import request_folder_path
from note_splitter.gui import require_folder_path
from note_splitter.gui import SplitSummaryDialog
from note_splitter.lexer import Lexer
from note_splitter.note import create_file_names
from note_splitter.note import create_notes
from note_splitter.note import ensure_file_path_uniqueness
from note_splitter.note import make_file_paths_absolute
from note_splitter.note import Note
from note_splitter.note import show_message
from note_splitter.note import validate_file_name
from note_splitter.parser_ import SyntaxTree
from note_splitter.settings import DEFAULT_SETTINGS
from note_splitter.settings import get_token_type
from note_splitter.settings import get_token_type_names
from note_splitter.settings import update_from_checkbox
from note_splitter.settings import update_from_combo_box
from note_splitter.settings import update_from_line_edit
from note_splitter.splitter import Splitter
from PySide6 import QtCore
from PySide6 import QtWidgets


class SplitTab(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.main_window = main_window
        settings = QtCore.QSettings()
        self.all_notes: list[Note] = []
        self.chosen_notes: list[Note] = []
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("Choose files to split:"))
        files_choosing_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(files_choosing_layout)
        self.browse_button = QtWidgets.QPushButton("browse")
        files_choosing_layout.addWidget(self.browse_button)
        self.browse_button.clicked.connect(self.__on_browse_button_click)
        files_choosing_layout.addWidget(QtWidgets.QLabel(" or "))
        self.keyword_search_button = QtWidgets.QPushButton("find by keyword")
        self.keyword_search_button.clicked.connect(self.__on_keyword_search)
        files_choosing_layout.addWidget(self.keyword_search_button)
        self.keyword_line_edit = QtWidgets.QLineEdit(
            settings.value("split_keyword", DEFAULT_SETTINGS["split_keyword"])
        )
        self.keyword_line_edit.editingFinished.connect(
            lambda: update_from_line_edit("split_keyword", self.keyword_line_edit)
        )
        files_choosing_layout.addWidget(self.keyword_line_edit)

        self.layout.addWidget(QtWidgets.QLabel("Files to split:"))
        self.file_list_text_browser = QtWidgets.QTextBrowser()
        self.layout.addWidget(self.file_list_text_browser)

        self.layout.addWidget(QtWidgets.QLabel("Choose what to split by:"))
        self.split_by_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.split_by_layout)
        self.type_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.type_layout)
        self.type_layout.addWidget(QtWidgets.QLabel("type:"))
        self.type_combo_box = QtWidgets.QComboBox()
        token_type_names: list[str] = get_token_type_names()
        token_type_names.remove("section")
        self.type_combo_box.addItems(token_type_names)
        self.type_combo_box.setCurrentText(
            settings.value("split_type", DEFAULT_SETTINGS["split_type"])
        )
        self.type_combo_box.currentTextChanged.connect(self.__on_split_type_change)
        self.type_layout.addWidget(self.type_combo_box)
        self.attribute_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.attribute_layout)
        self.attribute_layout.addWidget(QtWidgets.QLabel("attribute:"))
        split_attrs: dict = settings.value(
            "split_attrs", DEFAULT_SETTINGS["split_attrs"]
        )
        self.attribute_combo_box = QtWidgets.QComboBox()
        self.attribute_combo_box.setMinimumWidth(100)
        self.attribute_combo_box.addItems(self.__get_split_type_attr_names())
        if split_attrs:
            self.attribute_combo_box.setCurrentText(list(split_attrs.keys())[0])
        self.attribute_combo_box.currentTextChanged.connect(self.__on_split_attr_change)
        self.attribute_layout.addWidget(self.attribute_combo_box)
        self.value_layout = QtWidgets.QVBoxLayout()
        self.split_by_layout.addLayout(self.value_layout)
        self.value_layout.addWidget(QtWidgets.QLabel("value:"))
        self.value_line_edit = QtWidgets.QLineEdit()
        if split_attrs:
            self.value_line_edit.setText(str(list(split_attrs.values())[0]))
        self.value_line_edit.textChanged.connect(self.__on_split_value_change)
        self.value_layout.addWidget(self.value_line_edit)

        self.parse_blocks_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.parse_blocks_layout)
        self.parse_blocks_checkbox = QtWidgets.QCheckBox()
        self.parse_blocks_checkbox.setChecked(
            settings.value("parse_blocks", DEFAULT_SETTINGS["parse_blocks"])
        )
        self.parse_blocks_checkbox.stateChanged.connect(
            lambda: update_from_checkbox("parse_blocks", self.parse_blocks_checkbox)
        )
        self.parse_blocks_layout.addWidget(self.parse_blocks_checkbox)
        self.parse_blocks_layout.addWidget(QtWidgets.QLabel("parse blocks"))
        self.parse_blocks_layout.addStretch()

        self.split_button = QtWidgets.QPushButton("split")
        self.split_button.clicked.connect(self.__on_split_button_click)
        self.split_button.setStyleSheet("background-color: #225185;")
        self.layout.addWidget(self.split_button)
        self.layout.addStretch()

    def reload_tab_inputs(self) -> None:
        """Reloads the inputs on the tab from the settings.

        Uses the default settings as a fallback for any settings that are not found.
        """
        settings = QtCore.QSettings()
        self.keyword_line_edit.setText(
            settings.value("split_keyword", DEFAULT_SETTINGS["split_keyword"])
        )
        self.chosen_notes.clear()
        self.file_list_text_browser.clear()
        self.type_combo_box.setCurrentText(
            settings.value("split_type", DEFAULT_SETTINGS["split_type"])
        )
        if settings.contains("split_attrs") and settings.value("split_attrs"):
            self.attribute_combo_box.setCurrentText(
                list(settings.value("split_attrs"))[0]
            )
            self.value_line_edit.setText(
                str(list(settings.value("split_attrs").values())[0])
            )
        else:
            split_attrs: dict = DEFAULT_SETTINGS["split_attrs"]  # type: ignore
            self.attribute_combo_box.setCurrentText(list(split_attrs.keys())[0])
            self.value_line_edit.setText(str(list(split_attrs.values())[0]))
        self.parse_blocks_checkbox.setChecked(
            settings.value("parse_blocks", DEFAULT_SETTINGS["parse_blocks"])
        )

    def __on_browse_button_click(self) -> None:
        """Shows a file dialog and saves selected files into ``self.chosen_notes``."""
        settings = QtCore.QSettings()
        settings.setValue("using_split_keyword", 0)
        self.chosen_notes = files_browse(
            self,
            "choose files to split",
            settings.value("source_folder_path", None),
        )
        if self.chosen_notes:
            self.file_list_text_browser.setText(
                "\n".join(f"[[{n.name}]] {n.title}" for n in self.chosen_notes)
            )
        else:
            self.file_list_text_browser.clear()

    def __on_keyword_search(self) -> None:
        """Searches for files with the keyword and updates the file list."""
        keyword: str = self.keyword_line_edit.text()
        if not keyword:
            show_message("Please enter a keyword to search for.")
            return
        QtCore.QSettings().setValue("using_split_keyword", 1)
        self.all_notes = self.__get_all_notes_in_source_folder()
        if not self.all_notes:
            return
        self.chosen_notes = self.__get_notes_with_keyword(keyword, self.all_notes)
        if self.chosen_notes:
            self.file_list_text_browser.setText(
                "\n".join(f"[[{n.name}]] {n.title}" for n in self.chosen_notes)
            )
        else:
            show_message("No notes with the chosen keyword found.")
            self.file_list_text_browser.clear()

    def __on_split_type_change(self) -> None:
        update_from_combo_box("split_type", self.type_combo_box)
        self.attribute_combo_box.clear()
        attr_names: list[str] = self.__get_split_type_attr_names()
        self.attribute_combo_box.addItems(attr_names)
        if attr_names and attr_names[0] != "(none)":
            QtCore.QSettings().setValue("split_attrs", {attr_names[0]: ""})
        else:
            QtCore.QSettings().setValue("split_attrs", {})
        self.value_line_edit.clear()
        split_type: type[tokens.Token] = get_token_type(
            self.type_combo_box.currentText()
        )
        if issubclass(split_type, tokens.Block):
            self.parse_blocks_checkbox.setChecked(True)
            self.parse_blocks_checkbox.setEnabled(False)
        else:
            self.parse_blocks_checkbox.setEnabled(True)

    def __on_split_attr_change(self) -> None:
        current_text: str = self.attribute_combo_box.currentText()
        if current_text == "(none)":
            QtCore.QSettings().setValue("split_attrs", {})
        else:
            QtCore.QSettings().setValue("split_attrs", {current_text: ""})
        self.value_line_edit.clear()

    def __on_split_value_change(self) -> None:
        current_text: str = self.attribute_combo_box.currentText()
        if current_text == "(none)":
            QtCore.QSettings().setValue("split_attrs", {})
        else:
            QtCore.QSettings().setValue(
                "split_attrs", {current_text: self.value_line_edit.text()}
            )

    def __get_split_type_attr_names(self) -> list[str]:
        """Returns a list of attribute names of the split type.

        Also adds "(none)" to the list. Removes "_content" from the list if the split
        type is a block.
        """
        split_type: type[tokens.Token] = get_token_type(
            QtCore.QSettings().value("split_type", DEFAULT_SETTINGS["split_type"])
        )
        attr_names: list[str] = ["(none)"]
        if not inspect.isabstract(split_type):
            attr_names.extend(sorted(list(split_type().__dict__.keys())))
            if issubclass(split_type, tokens.Block):
                attr_names.remove("_content")
        return attr_names

    def __on_split_button_click(self) -> None:
        if not self.chosen_notes:
            show_message("No files chosen to split.")
            return
        if not self.all_notes:
            self.all_notes = self.__get_all_notes_in_source_folder()
        new_notes: list[Note] = self.__split_files(self.chosen_notes)
        self.all_notes.extend(new_notes)
        dialog = SplitSummaryDialog(new_notes, self.all_notes, self)
        dialog.exec()
        self.file_list_text_browser.clear()
        self.chosen_notes.clear()

    def __get_all_notes_in_source_folder(self) -> list[Note]:
        """Gets all the notes in the user's chosen source folder.

        If a source folder has not been chosen yet, the user will be asked to choose
        one.
        """
        folder_list: list[str]
        settings = QtCore.QSettings()
        source_folder_path: str | None = settings.value("source_folder_path")
        try:
            if not source_folder_path:
                raise FileNotFoundError
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
        assert source_folder_path is not None
        file_paths: list[str] = [
            os.path.join(source_folder_path, file_name) for file_name in folder_list
        ]
        return create_notes(file_paths)

    def __get_notes_with_keyword(
        self, split_keyword: str, all_notes: list[Note]
    ) -> list[Note]:
        """Filters to the notes that have the split keyword."""
        if not all_notes:
            all_notes = self.__get_all_notes_in_source_folder()
        if not all_notes:
            return []
        chosen_notes: list[Note] = []
        progress_dialog = QtWidgets.QProgressDialog(
            "searching for notes with the keyword",
            "cancel",
            0,
            len(all_notes),
            self,
            modal=True,
        )
        for i, note in enumerate(all_notes):
            progress_dialog.setValue(i)
            with open(note.path, "r", encoding="utf8") as file:
                contents = file.read()
            if split_keyword in contents:
                chosen_notes.append(note)
        progress_dialog.setValue(len(all_notes))
        return chosen_notes

    def __split_files(self, notes: list[Note] | None = None) -> list[Note]:
        """Splits files into multiple smaller files.

        If no notes are provided, they will be found using the split keyword and the
        source folder path chosen in settings.

        Parameters
        ----------
        notes : list[Note] | None
            The notes to be split. If None, notes will be found using the split keyword.

        Returns
        -------
        new_notes : list[Note]
            The newly created notes.
        """
        progress = QtWidgets.QProgressDialog(
            "splitting...", "cancel", 0, 100, self, modal=True
        )
        progress.forceShow()
        tokenize: Callable = Lexer()
        split: Callable = Splitter()
        format_: Callable = Formatter()

        settings = QtCore.QSettings()
        split_keyword: str = settings.value(
            "split_keyword", DEFAULT_SETTINGS["split_keyword"]
        )
        file_id_format: str = settings.value(
            "file_id_format", DEFAULT_SETTINGS["file_id_format"]
        )
        file_name_format: str = settings.value(
            "file_name_format", DEFAULT_SETTINGS["file_name_format"]
        )
        split_type: type[tokens.Token] = get_token_type(
            settings.value("split_type", DEFAULT_SETTINGS["split_type"])
        )
        split_attrs: dict = settings.value(
            "split_attrs", DEFAULT_SETTINGS["split_attrs"]
        )
        using_split_keyword: bool = bool(
            settings.value(
                "using_split_keyword", DEFAULT_SETTINGS["using_split_keyword"]
            )
        )
        remove_split_keyword: bool = bool(
            settings.value(
                "remove_split_keyword", DEFAULT_SETTINGS["remove_split_keyword"]
            )
        )
        parse_blocks: bool = bool(
            settings.value("parse_blocks", bool(DEFAULT_SETTINGS["parse_blocks"]))
        )
        copy_global_tags: bool = bool(
            settings.value(
                "copy_global_tags", bool(DEFAULT_SETTINGS["copy_global_tags"])
            )
        )
        copy_frontmatter: bool = bool(
            settings.value(
                "copy_frontmatter", bool(DEFAULT_SETTINGS["copy_frontmatter"])
            )
        )
        move_footnotes: bool = bool(
            settings.value("move_footnotes", bool(DEFAULT_SETTINGS["move_footnotes"]))
        )
        create_index_file: bool = bool(
            settings.value("create_index_file", DEFAULT_SETTINGS["create_index_file"])
        )
        create_backlinks: bool = bool(
            settings.value("create_backlinks", DEFAULT_SETTINGS["create_backlinks"])
        )

        progress.setValue(1)
        if not notes:
            notes = self.__get_notes_with_keyword(split_keyword, self.all_notes)
        if not notes:
            return []
        all_new_notes: list[Note] = []

        note_count = len(notes)
        for i, source_note in enumerate(notes):
            progress.setValue((i + 1) / (note_count + 5) * 100)
            with open(source_note.path, "r", encoding="utf8") as file:
                content: str = file.read()
            progress.setValue((i + 2) / (note_count + 5) * 100)
            split_contents: list[str] = split_text(
                content,
                tokenize,
                split,
                format_,
                split_type,
                split_attrs,
                using_split_keyword,
                remove_split_keyword,
                split_keyword,
                parse_blocks,
                copy_global_tags,
                copy_frontmatter,
                move_footnotes,
            )
            progress.setValue((i + 3) / (note_count + 5) * 100)
            new_file_names: list[str] = create_file_names(
                source_note.ext, file_id_format, file_name_format, split_contents
            )
            progress.setValue((i + 4) / (note_count + 5) * 100)
            new_notes = self.save_new_notes(split_contents, new_file_names)
            all_new_notes.extend(new_notes)
            progress.setValue((i + 5) / (note_count + 5) * 100)
            print(f"Created {len(new_notes)} new files.")
            if new_notes:
                if create_index_file:
                    index_note: Note = create_index_file_(
                        source_note, new_notes, split_type
                    )
                    print(f"Created index file at {index_note.path}")
                    all_new_notes.append(index_note)
                    if create_backlinks:
                        append_backlinks(index_note, new_notes)
                elif create_backlinks:
                    append_backlinks(source_note, new_notes)
        progress.cancel()
        return all_new_notes

    def save_new_notes(
        self, split_contents: list[str], new_file_names: list[str]
    ) -> list[Note]:
        """Creates new files and saves strings into them.

        The lists for the contents and names of the new files are parallel.

        Attributes
        ----------
        split_contents : list[str]
            A list of strings to each be saved into a new file.
        new_file_names : list[str]
            A list of names of files to be created.

        Returns
        -------
        new_notes : list[Note]
            The newly created notes.
        """
        new_notes = []
        settings = QtCore.QSettings()
        source_folder_path: str | None = settings.value("source_folder_path")
        destination_folder_path: str | None = settings.value("destination_folder_path")
        if not destination_folder_path or not os.path.exists(destination_folder_path):
            destination_folder_path = require_folder_path("destination")
            settings.setValue("destination_folder_path", destination_folder_path)
            self.main_window.settings_tab.destination_folder_line_edit.setText(
                destination_folder_path
            )

        for new_file_name, split_content in zip(new_file_names, split_contents):
            new_file_path: str = ensure_file_path_uniqueness(
                os.path.join(destination_folder_path, new_file_name)
            )
            if not source_folder_path or source_folder_path != destination_folder_path:
                split_content = make_file_paths_absolute(split_content, new_file_path)
            with open(new_file_path, "x", encoding="utf8") as file:
                file.write(split_content)
            new_notes.append(Note(new_file_path))
        return new_notes


def split_text(
    content: str,
    tokenize: Callable,
    split: Callable,
    format_: Callable,
    split_type: type[tokens.Token],
    split_attrs: dict,
    using_split_keyword: bool,
    remove_split_keyword: bool,
    split_keyword: str,
    parse_blocks: bool,
    copy_global_tags: bool,
    copy_frontmatter: bool,
    move_footnotes: bool,
) -> list[str]:
    """Splits a string into multiple strings based on several factors.

    Attributes
    ----------
    content : str
        The string to be split.
    tokenize : Callable
        A function created from the Lexer class that converts a string into a list of
        tokens.
    split : Callable
        A function created from the Splitter class that groups the tokens into sections.
    format_ : Callable
        A function created from the Formatter class that adjusts the formatting of each
        section and converts them to strings.
    split_type : type[tokens.Token]
        The type of token to split by.
    split_attrs : dict
        The attributes of the token to split by.
    using_split_keyword : bool
        Whether to use a keyword to decide which files to split.
    remove_split_keyword : bool
        Whether to remove the keyword from the content of the token.
    split_keyword : str
        The keyword for deciding which files to split.
    parse_blocks : bool
        Whether to parse blocks.
    copy_global_tags : bool
        Whether to copy global tags to each new file.
    copy_frontmatter : bool
        Whether to copy frontmatter to each new file.
    move_footnotes : bool
        Whether to move footnotes into the new files.

    Returns
    -------
    split_contents : list[str]
        A list of strings that are the sections of the original string.
    """
    tokens_: list[tokens.Token] = tokenize(content)
    syntax_tree = SyntaxTree(tokens_, parse_blocks)
    sections, global_tags = split(
        syntax_tree.content,
        split_type,
        split_attrs,
        using_split_keyword,
        remove_split_keyword,
        split_keyword,
    )
    split_contents: list[str] = format_(
        sections=sections,
        global_tags=global_tags,
        copy_global_tags=copy_global_tags,
        copy_frontmatter=copy_frontmatter,
        move_footnotes=move_footnotes,
        frontmatter=syntax_tree.frontmatter,
        footnotes=syntax_tree.footnotes,
    )
    return split_contents


def create_index_file_(
    source_note: Note, new_notes: list[Note], split_type: type[tokens.Token]
) -> Note:
    """Creates an index file for the new notes in the same folder.

    Parameters
    ----------
    source_note : Note
        The note that the new notes were created from.
    new_notes : list[Note]
        The newly created notes.
    split_type : type[tokens.Token]
        The type of token that was split by.

    Returns
    -------
    Note
        The newly created index note.
    """
    index_name = validate_file_name(f"index - {source_note.name}", 35)
    folder_path = new_notes[0].folder_path
    index_file_path = os.path.join(folder_path, index_name)
    index_file_path = ensure_file_path_uniqueness(index_file_path)
    with open(index_file_path, "x", encoding="utf8") as file:
        file.write(f"# index of {source_note.title}\n\n")
        for n in new_notes:
            if issubclass(split_type, tokens.Header):
                file.write(f"* [{n.title}]({n.path})\n")
            else:
                file.write(f"* [{n.name}]({n.path})\n")
        file.write(f"\n[Source: {source_note.title}]({source_note.path})")
    return Note(index_file_path, folder_path, index_name)


def append_backlinks(root_note: Note, notes: list[Note]) -> None:
    """Appends backlinks to the root note in each of the given notes.

    Parameters
    ----------
    root_note : str
        The note that the backlinks will link to.
    notes : list[Note]
        The notes to append backlinks to.
    """
    for note_ in notes:
        with open(note_.path, "a", encoding="utf8") as file:
            file.write(f"\n\n[Backlink: {root_note.title}]({root_note.path})\n")

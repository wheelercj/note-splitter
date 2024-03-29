"""Various functions for building the graphical user interface."""
from note_splitter.note import create_notes
from note_splitter.note import Note
from note_splitter.settings import DEFAULT_SETTINGS
from note_splitter.settings import show_message
from PySide6 import QtCore
from PySide6 import QtWidgets


def request_confirmation(text: str) -> bool:
    """Asks for confirmation from the user.

    Returns True if the user chooses "Yes", False otherwise.
    """
    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowTitle("confirm")
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    return msg_box.exec() == QtWidgets.QMessageBox.Yes


def folder_browse(
    parent: QtWidgets.QWidget, line_edit: QtWidgets.QLineEdit, title: str
) -> str:
    """Opens a folder dialog, sets the line edit's text, & emits ``editingFinished``.

    If the user cancels the dialog, the line edit's text is not changed, the signal
    is not emitted, and an empty string is returned. Only folders are shown in the
    dialog.
    """
    folder_path: str = QtWidgets.QFileDialog.getExistingDirectory(
        parent, title, QtCore.QDir.currentPath(), QtWidgets.QFileDialog.ShowDirsOnly
    )
    if folder_path:
        line_edit.setText(folder_path)
        line_edit.editingFinished.emit()
    return folder_path


def files_browse(
    parent: QtWidgets.QWidget | None, title: str, start_folder_path: str | None = None
) -> list[Note]:
    """Opens a file dialog and returns the selected notes.

    If the user cancels the dialog, an empty list is returned.

    Parameters
    ----------
    parent : QtWidgets.QWidget | None
        The parent widget. If not None, the dialog will be centered over the parent.
    title : str
        The title of the dialog.
    start_folder_path : str | None
        The folder path that the dialog will open to. If None, the current working
        directory is used.
    """
    if not start_folder_path:
        start_folder_path = QtCore.QDir.currentPath()
    return create_notes(
        QtWidgets.QFileDialog.getOpenFileNames(
            parent,
            title,
            start_folder_path,
            "Text Files (*.txt *.md *.rst);;All Files (*)",
        )[0]
    )


def require_folder_path(folder_description: str) -> str:
    """Requires the user to choose a folder.

    Parameters
    ----------
    folder_description : str
        The description of the folder that the user will be choosing.

    Returns
    -------
    str
        The absolute path to a folder.
    """
    while True:
        folder_path = request_folder_path(folder_description)
        if folder_path:
            return folder_path


def request_folder_path(folder_description: str) -> str | None:
    """Prompts the user to select a folder.

    Parameters
    ----------
    folder_description : str
        The description of the folder.

    Returns
    -------
    str, None
        The absolute path to a folder, or None if the user canceled.
    """
    message = f"Please select the {folder_description} folder."
    folder_path: str = QtWidgets.QFileDialog.getExistingDirectory(
        None, message, QtCore.QDir.currentPath(), QtWidgets.QFileDialog.ShowDirsOnly
    )
    if not folder_path:
        return None
    return folder_path


class SplitSummaryDialog(QtWidgets.QDialog):
    def __init__(
        self, new_notes: list[Note], all_notes: list[Note], parent: QtWidgets.QWidget
    ):
        super().__init__(parent, QtCore.Qt.WindowType.Window)
        self.new_notes = new_notes
        self.all_notes = all_notes
        self.layout = QtWidgets.QVBoxLayout(self)
        self.note_count_label = QtWidgets.QLabel(f"{len(self.new_notes)} files created")
        self.layout.addWidget(self.note_count_label)
        self.notes_list_widget = QtWidgets.QListWidget()
        self.notes_list_widget.addItems(
            f"[[{n.name}]] {n.title}" for n in self.new_notes
        )
        self.notes_list_widget.setMinimumWidth(600)
        self.notes_list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        )
        group_box_layout = QtWidgets.QVBoxLayout()
        group_box_layout.addWidget(self.notes_list_widget)
        notes_buttons_layout = QtWidgets.QHBoxLayout()
        group_box_layout.addLayout(notes_buttons_layout)
        self.open_button = QtWidgets.QPushButton("open")
        self.open_button.clicked.connect(self.__open_notes)
        notes_buttons_layout.addWidget(self.open_button)
        self.delete_button = QtWidgets.QPushButton("delete")
        self.delete_button.clicked.connect(self.__delete_notes)
        notes_buttons_layout.addWidget(self.delete_button)
        self.move_button = QtWidgets.QPushButton("move")
        self.move_button.clicked.connect(self.__move_notes)
        notes_buttons_layout.addWidget(self.move_button)
        self.show_in_file_browser_button = QtWidgets.QPushButton("show in file browser")
        self.show_in_file_browser_button.clicked.connect(self.__show_notes)
        notes_buttons_layout.addWidget(self.show_in_file_browser_button)
        group_box = QtWidgets.QGroupBox()
        group_box.setLayout(group_box_layout)
        self.layout.addWidget(group_box)
        self.ok_button = QtWidgets.QPushButton("ok")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def __open_notes(self) -> None:
        """Opens the selected notes for the user to view."""
        selected_items: list[
            QtWidgets.QListWidgetItem
        ] = self.notes_list_widget.selectedItems()
        if not selected_items:
            show_message("No notes selected.")
            return
        for note_list_widget_item in selected_items:
            note_title: str = "]]".join(
                note_list_widget_item.text().split("]]", 1)[1:]
            )[1:]
            note: Note
            for note in self.new_notes:
                if note.title == note_title:
                    break
            note.open()

    def __delete_notes(self) -> None:
        """Moves the selected notes to the trash."""
        selected_items: list[
            QtWidgets.QListWidgetItem
        ] = self.notes_list_widget.selectedItems()
        if not selected_items:
            show_message("No notes selected.")
            return
        if not request_confirmation(
            "Are you sure you want to delete the selected notes?"
        ):
            return
        for note_list_widget_item in selected_items:
            note_title: str = "]]".join(
                note_list_widget_item.text().split("]]", 1)[1:]
            )[1:]
            note: Note
            for note in self.new_notes:
                if note.title == note_title:
                    break
            note.delete()
            self.new_notes.remove(note)
            self.notes_list_widget.takeItem(
                self.notes_list_widget.row(note_list_widget_item)
            )

    def __move_notes(self) -> None:
        """Moves the selected notes and updates internal links to them."""
        selected_items: list[
            QtWidgets.QListWidgetItem
        ] = self.notes_list_widget.selectedItems()
        if not selected_items:
            show_message("No notes selected.")
            return
        if destination := request_folder_path("destination"):
            note_types: list[str] = QtCore.QSettings().value(
                "note_types", DEFAULT_SETTINGS["note_types"]
            )
            for note_list_widget_item in selected_items:
                note_title: str = "]]".join(
                    note_list_widget_item.text().split("]]", 1)[1:]
                )[1:]
                note: Note
                for note in self.new_notes:
                    if note.title == note_title:
                        break
                note.move(destination, self.all_notes, note_types)
                self.new_notes.remove(note)
                self.notes_list_widget.takeItem(
                    self.notes_list_widget.row(note_list_widget_item)
                )

    def __show_notes(self) -> None:
        """Shows the selected notes in the file browser."""
        selected_items: list[
            QtWidgets.QListWidgetItem
        ] = self.notes_list_widget.selectedItems()
        if not selected_items:
            show_message("No notes selected.")
            return
        for note_list_widget_item in selected_items:
            note_title: str = "]]".join(
                note_list_widget_item.text().split("]]", 1)[1:]
            )[1:]
            note: Note
            for note in self.new_notes:
                if note.title == note_title:
                    break
            note.show()

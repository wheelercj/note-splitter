import re

from note_splitter.gui import folder_browse
from note_splitter.settings import DEFAULT_SETTINGS
from note_splitter.settings import export_settings
from note_splitter.settings import import_settings
from note_splitter.settings import reset_settings
from note_splitter.settings import update_from_checkbox
from note_splitter.settings import update_from_line_edit
from PySide6 import QtCore
from PySide6 import QtWidgets


class SettingsTab(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        settings = QtCore.QSettings()

        self.source_folder_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.source_folder_layout)
        self.source_folder_layout.addWidget(QtWidgets.QLabel("source folder:"))
        self.source_folder_line_edit = QtWidgets.QLineEdit(
            settings.value("source_folder_path", DEFAULT_SETTINGS["source_folder_path"])
        )
        self.source_folder_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "source_folder_path", self.source_folder_line_edit
            )
        )
        self.source_folder_layout.addWidget(self.source_folder_line_edit)
        self.source_folder_browse_button = QtWidgets.QPushButton("browse")
        self.source_folder_layout.addWidget(self.source_folder_browse_button)
        self.source_folder_layout.addStretch()

        self.destination_folder_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.destination_folder_layout)
        self.destination_folder_layout.addWidget(
            QtWidgets.QLabel("destination folder:")
        )
        self.destination_folder_line_edit = QtWidgets.QLineEdit(
            settings.value(
                "destination_folder_path", DEFAULT_SETTINGS["destination_folder_path"]
            )
        )
        self.destination_folder_line_edit.editingFinished.connect(
            lambda: update_from_line_edit(
                "destination_folder_path", self.destination_folder_line_edit
            )
        )
        self.destination_folder_layout.addWidget(self.destination_folder_line_edit)
        self.destination_folder_browse_button = QtWidgets.QPushButton("browse")
        self.destination_folder_browse_button.clicked.connect(
            lambda: folder_browse(
                self,
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
        self.new_file_name_format_line_edit = QtWidgets.QLineEdit(
            settings.value("file_name_format", DEFAULT_SETTINGS["file_name_format"])
        )
        self.new_file_name_format_line_edit.textChanged.connect(
            self.__on_file_name_format_change
        )
        self.file_name_format_layout.addWidget(self.new_file_name_format_line_edit)
        self.file_name_format_layout.addStretch()

        self.invalid_file_name_symbol_label = QtWidgets.QLabel(
            "You cannot use !@#$&*+={}|\\/:'\"<>?` in the file name format."
        )
        self.layout.addWidget(self.invalid_file_name_symbol_label)
        self.invalid_file_name_symbol_label.setStyleSheet("color: red")
        self.invalid_file_name_symbol_label.setMaximumHeight(20)
        self.invalid_file_name_symbol_label.hide()

        self.invalid_file_name_edge_symbol_label = QtWidgets.QLabel(
            "You cannot use ._- nor space at the start or end of the file name format."
        )
        self.layout.addWidget(self.invalid_file_name_edge_symbol_label)
        self.invalid_file_name_edge_symbol_label.setStyleSheet("color: red")
        self.invalid_file_name_edge_symbol_label.setMaximumHeight(20)
        self.invalid_file_name_edge_symbol_label.hide()

        self.invalid_file_name_variable_label = QtWidgets.QLabel(
            r"Valid uses of %: %uuid4, %title, %Y, %M, %D, %h, %m, %s, %id"
        )
        self.layout.addWidget(self.invalid_file_name_variable_label)
        self.invalid_file_name_variable_label.setStyleSheet("color: red")
        self.invalid_file_name_variable_label.setMaximumHeight(20)
        self.invalid_file_name_variable_label.hide()

        self.checkboxes_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(self.checkboxes_layout)
        self.create_index_file_checkbox = QtWidgets.QCheckBox()
        self.create_index_file_checkbox.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.create_index_file_checkbox.stateChanged.connect(
            lambda: update_from_checkbox(
                "create_index_file", self.create_index_file_checkbox
            )
        )
        self.checkboxes_layout.addRow(
            "create index file:", self.create_index_file_checkbox
        )
        self.create_index_file_checkbox.setChecked(
            settings.value("create_index_file", DEFAULT_SETTINGS["create_index_file"])
        )
        self.remove_split_keyword_checkbox = QtWidgets.QCheckBox()
        self.remove_split_keyword_checkbox.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.remove_split_keyword_checkbox.stateChanged.connect(
            lambda: update_from_checkbox(
                "remove_split_keyword", self.remove_split_keyword_checkbox
            )
        )
        self.checkboxes_layout.addRow(
            "remove split keyword:", self.remove_split_keyword_checkbox
        )
        self.remove_split_keyword_checkbox.setChecked(
            settings.value(
                "remove_split_keyword", DEFAULT_SETTINGS["remove_split_keyword"]
            )
        )
        self.move_footnotes_checkbox = QtWidgets.QCheckBox()
        self.move_footnotes_checkbox.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.move_footnotes_checkbox.stateChanged.connect(
            lambda: update_from_checkbox("move_footnotes", self.move_footnotes_checkbox)
        )
        self.checkboxes_layout.addRow("move footnotes:", self.move_footnotes_checkbox)
        self.move_footnotes_checkbox.setChecked(
            settings.value("move_footnotes", DEFAULT_SETTINGS["move_footnotes"])
        )
        self.copy_frontmatter_checkbox = QtWidgets.QCheckBox()
        self.copy_frontmatter_checkbox.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.copy_frontmatter_checkbox.stateChanged.connect(
            lambda: update_from_checkbox(
                "copy_frontmatter", self.copy_frontmatter_checkbox
            )
        )
        self.checkboxes_layout.addRow(
            "copy frontmatter:", self.copy_frontmatter_checkbox
        )
        self.copy_frontmatter_checkbox.setChecked(
            settings.value("copy_frontmatter", DEFAULT_SETTINGS["copy_frontmatter"])
        )
        self.copy_global_tags_checkbox = QtWidgets.QCheckBox()
        self.copy_global_tags_checkbox.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.copy_global_tags_checkbox.stateChanged.connect(
            lambda: update_from_checkbox(
                "copy_global_tags", self.copy_global_tags_checkbox
            )
        )
        self.checkboxes_layout.addRow(
            "copy global tags:", self.copy_global_tags_checkbox
        )
        self.copy_global_tags_checkbox.setChecked(
            settings.value("copy_global_tags", DEFAULT_SETTINGS["copy_global_tags"])
        )
        self.create_backlinks_checkbox = QtWidgets.QCheckBox()
        self.create_backlinks_checkbox.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.create_backlinks_checkbox.stateChanged.connect(
            lambda: update_from_checkbox(
                "create_backlinks", self.create_backlinks_checkbox
            )
        )
        self.checkboxes_layout.addRow(
            "create backlinks:", self.create_backlinks_checkbox
        )
        self.create_backlinks_checkbox.setChecked(
            settings.value("create_backlinks", DEFAULT_SETTINGS["create_backlinks"])
        )

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.export_button = QtWidgets.QPushButton("export")
        self.buttons_layout.addWidget(self.export_button)
        self.export_button.clicked.connect(export_settings)
        self.export_button.setToolTip("Export the settings to a JSON file.")

        self.import_button = QtWidgets.QPushButton("import")
        self.buttons_layout.addWidget(self.import_button)
        self.import_button.clicked.connect(self.__on_settings_import)
        self.import_button.setToolTip("Import the settings from a JSON file.")
        self.import_button.setStyleSheet("background-color: red")

        self.reset_button = QtWidgets.QPushButton("reset")
        self.buttons_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.__on_settings_reset)
        self.reset_button.setToolTip(
            "Reset the settings on ALL tabs to their defaults."
        )
        self.reset_button.setStyleSheet("background-color: red")

    def __on_file_name_format_change(self) -> None:
        if re.search(
            r"[!@#$&*+={}|\\/:'\"<>?`]", self.new_file_name_format_line_edit.text()
        ):
            self.new_file_name_format_line_edit.setStyleSheet("border: 1px solid red")
            self.invalid_file_name_symbol_label.show()
        elif re.search(r"^[ ._-]|[ ._-]$", self.new_file_name_format_line_edit.text()):
            self.new_file_name_format_line_edit.setStyleSheet("border: 1px solid red")
            self.invalid_file_name_edge_symbol_label.show()
        elif re.search(
            r"%(?!uuid4|title|Y|M|D|h|m|s|id)",
            self.new_file_name_format_line_edit.text(),
        ):
            self.new_file_name_format_line_edit.setStyleSheet("border: 1px solid red")
            self.invalid_file_name_variable_label.show()
        else:
            self.new_file_name_format_line_edit.setStyleSheet("")
            self.invalid_file_name_symbol_label.hide()
            self.invalid_file_name_edge_symbol_label.hide()
            self.invalid_file_name_variable_label.hide()
            update_from_line_edit(
                "file_name_format", self.new_file_name_format_line_edit
            )

    def __on_settings_import(self) -> None:
        import_settings()
        self.__reload_tab_inputs()
        self.main_window.central_widget.home_tab.reload_tab_inputs()
        self.main_window.central_widget.patterns_tab.reload_tab_inputs()

    def __on_settings_reset(self) -> None:
        """Resets all settings to their defaults and reloads the inputs on all tabs.

        Asks for confirmation first. This is a destructive action that cannot be undone
        and affects all tabs. Uses the default settings as a fallback for any settings
        that are not found.
        """
        if not self.__confirm_settings_reset():
            return
        reset_settings()
        self.__reload_tab_inputs()
        self.main_window.central_widget.home_tab.reload_tab_inputs()
        self.main_window.central_widget.patterns_tab.reload_tab_inputs()

    def __confirm_settings_reset(self) -> bool:
        """Asks for confirmation before resetting all settings.

        Returns True if the user confirms the reset, False otherwise.
        """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("reset settings")
        msg_box.setText("This will reset the settings on ALL tabs to their defaults.")
        msg_box.setInformativeText("Are you sure you want to reset the settings?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
        return msg_box.exec() == QtWidgets.QMessageBox.Yes

    def __reload_tab_inputs(self) -> None:
        """Reloads the inputs on the tab from the settings.

        Uses the default settings as a fallback for any settings that are not found.
        """
        settings = QtCore.QSettings()
        self.source_folder_line_edit.setText(
            settings.value("source_folder_path", DEFAULT_SETTINGS["source_folder_path"])
        )
        self.destination_folder_line_edit.setText(
            settings.value(
                "destination_folder_path", DEFAULT_SETTINGS["destination_folder_path"]
            )
        )
        self.new_file_name_format_line_edit.setText(
            settings.value("file_name_format", DEFAULT_SETTINGS["file_name_format"])
        )
        self.create_index_file_checkbox.setChecked(
            settings.value("create_index_file", DEFAULT_SETTINGS["create_index_file"])
        )
        self.remove_split_keyword_checkbox.setChecked(
            settings.value(
                "remove_split_keyword", DEFAULT_SETTINGS["remove_split_keyword"]
            )
        )
        self.move_footnotes_checkbox.setChecked(
            settings.value("move_footnotes", DEFAULT_SETTINGS["move_footnotes"])
        )
        self.copy_frontmatter_checkbox.setChecked(
            settings.value("copy_frontmatter", DEFAULT_SETTINGS["copy_frontmatter"])
        )
        self.copy_global_tags_checkbox.setChecked(
            settings.value("copy_global_tags", DEFAULT_SETTINGS["copy_global_tags"])
        )
        self.create_backlinks_checkbox.setChecked(
            settings.value("create_backlinks", DEFAULT_SETTINGS["create_backlinks"])
        )

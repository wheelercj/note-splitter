import os

from note_splitter.menu import Menu
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Splitter")
        if os.path.exists("app"):
            self.setWindowIcon(
                QtGui.QIcon("app/note_splitter/resources/note_splitter.svg")
            )
        else:
            self.setWindowIcon(
                QtGui.QIcon("src/note_splitter/resources/note_splitter.svg")
            )
        self.central_widget = Menu(self)
        self.setCentralWidget(self.central_widget)
        self.is_quitting = False
        qApp.aboutToQuit.connect(self.__on_quit)  # type: ignore # noqa: F821
        self.__load_settings_and_show_window()
        self.close_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)

    def __on_quit(self) -> None:
        """Called when the application is about to quit.

        Other code may run for a short time after this method runs.
        """
        self.is_quitting = True
        settings = QtCore.QSettings()
        settings.setValue("main_window/geometry", self.saveGeometry())

    def __load_settings_and_show_window(self):
        """Reads the settings from the device's configuration files."""
        settings = QtCore.QSettings()
        if not settings.contains("main_window/geometry"):
            self.showMaximized()
        else:
            geometry_bytes: QtCore.QByteArray = settings.value("main_window/geometry")
            if geometry_bytes.isEmpty():
                self.showMaximized()
            else:
                self.adjustSize()
                self.restoreGeometry(geometry_bytes)
                self.show()

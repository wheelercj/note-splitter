from note_splitter.menu import Menu
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Splitter")
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
        # TODO: save other settings.

    def __load_settings_and_show_window(self):
        """Reads the settings from the device's configuration files."""
        settings = QtCore.QSettings()
        # TODO: load other settings.
        # if settings.contains("user/email") and settings.contains("user/password"):
        #     user.email = str(settings.value("user/email"))
        #     user.password = str(settings.value("user/password"))
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

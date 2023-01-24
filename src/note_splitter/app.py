import sys
from importlib import metadata as importlib_metadata

from note_splitter.main_window import MainWindow
from PySide6 import QtWidgets


def main():
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PySide2
    # this is set with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])
    QtWidgets.QApplication.setOrganizationDomain(
        "https://github.com/wheelercj/note-splitter"
    )
    QtWidgets.QApplication.setOrganizationName("Note Splitter")

    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget {
            font-size: 14px;
        }
        """
    )
    main_window = MainWindow()  # noqa: F841
    sys.exit(app.exec())

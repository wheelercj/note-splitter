from note_splitter.about_tab import AboutTab
from note_splitter.home_tab import HomeTab
from note_splitter.patterns_tab import PatternsTab
from note_splitter.settings_tab import SettingsTab
from PySide6 import QtWidgets


class Menu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.tab_widget = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.home_tab = HomeTab(self)
        self.tab_widget.addTab(self.home_tab, "home")
        self.settings_tab = SettingsTab(main_window)
        self.tab_widget.addTab(self.settings_tab, "settings")
        self.patterns_tab = PatternsTab()
        self.tab_widget.addTab(self.patterns_tab, "patterns")
        self.about_tab = AboutTab()
        self.tab_widget.addTab(self.about_tab, "about")

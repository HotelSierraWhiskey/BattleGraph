from qtstrap import *
from menu import MainMenuBar
from graphing import Graph


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.infile = None

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.current_file_label = QLabel('')

        self.main_menu = MainMenuBar()
        self.graph = Graph()

        self.main_menu.file_submenu.infile_changed.connect(self.update_infile)
        self.main_menu.file_submenu.infile_changed.connect(self.graph.update)
        self.graph.infile_changed.connect(self.update_infile)

        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(self.main_menu)
                    layout.add(self.current_file_label)
                    layout.add(self.graph)

    def update_infile(self, fname):
        self.infile = fname
        self.current_file_label.setText(self.infile)

    






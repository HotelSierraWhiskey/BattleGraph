from bs4 import BeautifulSoup
from qtstrap import *
from menu import MainMenuBar
from graphing import Graph


class MainWindow(BaseMainWindow):
    def __init__(self, quit_application_callback, parent=None):
        super().__init__(parent=parent)

        self.infile = None

        self.quit = quit_application_callback

        self.setAcceptDrops(True)
        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.current_file_label = QLabel('')

        main_menu_callbacks = {
            'quit_application_callback': self.quit,
            'change_current_file_label_callback': self.current_file_label.setText,
            'get_current_file_label_callback': self.current_file_label.text
        }

        self.main_menu = MainMenuBar(main_menu_callbacks)
        self.graph = Graph()


        self.main_menu.file_submenu.infile_changed.connect(self.update_infile)
        self.main_menu.file_submenu.infile_changed.connect(self.graph.update)


        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(self.main_menu)
                    layout.add(self.current_file_label)
                    layout.add(self.graph)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            fname = event.mimeData().urls()[0].url()
            self.infile = fname
            self.current_file_label.setText(fname)

    def update_infile(self, fname):
        self.infile = fname
        self.current_file_label.setText(self.infile)

    






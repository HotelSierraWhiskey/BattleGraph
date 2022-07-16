from qtstrap import *
from menu import MainMenuBar
from graphing import FileViewer, PieChart



class SearchWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = QLineEdit()
        self.search_button = QPushButton('Search')
        self.clear_button = QPushButton('Clear Selections')
        
        self.field.setMaximumWidth(250)
        self.search_button.setMaximumWidth(75)
        self.clear_button.setMaximumWidth(150)


        with CVBoxLayout(self) as layout:
            with layout.hbox(align='right') as layout:
                layout.add(self.field)
                layout.add(self.search_button)
                layout.add(self.clear_button)
            


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.infile = None

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.current_file_label = QLabel('No file selected')
        self.status_label = QLabel('')
        self.status_label.setMinimumHeight(45)
        self.search_widget = SearchWidget()

        self.main_menu = MainMenuBar()

        self.file_viewer = FileViewer()
        self.pie_chart = PieChart()


        self.tab_objects = {'File Viewer': self.file_viewer, 
                            'Slot Distribution': self.pie_chart}
        
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        for k, v in self.tab_objects.items():
            self.tabs.addTab(v, k)

        self.main_menu.file_submenu.infile_changed.connect(self.update)
        self.main_menu.file_submenu.infile_changed.connect(self.pie_chart.update)
        self.main_menu.file_submenu.infile_changed.connect(self.file_viewer.update)
        self.main_menu.file_submenu.status_update.connect(self.status_label.setText)
        self.main_menu.file_submenu.export_requested.connect(self.pie_chart.save_image)

        self.pie_chart.infile_changed.connect(self.update)

        self.file_viewer.infile_changed.connect(self.update)
        self.file_viewer.search_requested.connect(self.search_widget.field.clear)

        self.search_widget.search_button.clicked.connect(lambda: self.file_viewer.find(self.search_widget.field.text()))
        self.search_widget.clear_button.clicked.connect(self.file_viewer.clear)

        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(self.main_menu)
                    with layout.hbox() as layout:
                        layout.add(self.current_file_label)
                        layout.add(self.status_label)
                        layout.add(self.search_widget)
                    layout.add(self.tabs)

    def update(self, fname):
        self.infile = fname
        self.main_menu.file_submenu.filename = self.infile
        for tab in self.tab_objects.values():
            tab.update(self.infile)
        
        self.current_file_label.setText(self.infile)
        self.file_viewer.clear()

    def handle_tab_change(self):
        if self.tabs.currentWidget() != self.file_viewer:
            self.search_widget.setHidden(True)
            return
        self.search_widget.setHidden(False)
        
    






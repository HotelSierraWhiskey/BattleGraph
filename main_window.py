from qtstrap import *
from menu import MainMenuBar
from graphing import FileViewer, PieChart


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.infile = None

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.current_file_label = QLabel('No file selected')

        self.main_menu = MainMenuBar()

        self.file_viewer = FileViewer()
        self.pie_chart = PieChart()

        self.tab_objects = {'File Viewer': self.file_viewer, 
                            'Slot Distribution': self.pie_chart}
        
        self.tabs = QTabWidget()
        
        for k, v in self.tab_objects.items():
            self.tabs.addTab(v, k)

        self.main_menu.file_submenu.infile_changed.connect(self.update)
        self.main_menu.file_submenu.infile_changed.connect(self.pie_chart.update)
        self.main_menu.file_submenu.infile_changed.connect(self.file_viewer.update)
        self.main_menu.file_submenu.export_requested.connect(self.pie_chart.save_image)

        self.pie_chart.infile_changed.connect(self.update)
        self.file_viewer.infile_changed.connect(self.update)

        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(self.main_menu)
                    layout.add(self.current_file_label)
                    layout.add(self.tabs)

    def update(self, fname):
        self.infile = fname
        self.current_file_label.setText(self.infile)
        for tab in self.tab_objects.values():
            tab.update(self.infile)

    






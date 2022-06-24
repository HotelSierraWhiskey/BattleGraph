from audioop import add
from qtstrap import *


class FileMenu(QMenu):

    infile_changed = Signal(str)
    quit_application = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(title='File', *args, **kwargs)

        self.filename = None
        self.addAction('Import File', self.open_file_dialog)
        self.addAction('Save Image')
        self.addAction('Export PDF')
        self.addSeparator()
        self.addAction('Quit', self.quit_application.emit)

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File')
        if fname:
            self.filename = fname[0]
            self.infile_changed.emit(self.filename)
            


class MainMenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.file_submenu = FileMenu()

        self.addMenu(self.file_submenu)
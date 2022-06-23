from audioop import add
from qtstrap import *


class FileMenu(QMenu):
    def __init__(self, callbacks, *args, **kwargs):
        super().__init__(title='File', *args, **kwargs)
        self.callbacks = callbacks
        self.filename = None
        self.addAction('Import File', self.open_file_dialog)
        self.addAction('Save Image')
        self.addAction('Export PDF')
        self.addSeparator()
        self.addAction('Quit', lambda: self.callbacks['quit_application_callback']())

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File')
        if fname:
            self.filename = fname[0]
            self.callbacks['change_current_file_label_callback'](self.filename)





class MainMenuBar(QMenuBar):
    def __init__(self, callbacks, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callbacks = callbacks

        file_submenu_callbacks = {
            'quit_application_callback': self.callbacks['quit_application_callback'],
            'change_current_file_label_callback': self.callbacks['change_current_file_label_callback']
        }

        file_submenu = FileMenu(file_submenu_callbacks)

        self.addMenu(file_submenu)
from qtstrap import *
import os
from threading import Thread
import time
import shutil
from bs4 import BeautifulSoup
import weasyprint


class FileMenu(QMenu):

    infile_changed = Signal(str)
    quit_application = Signal()
    export_requested = Signal(str)
    status_update = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(title='File', *args, **kwargs)

        self.filename = None
        self.addAction('Import File', self.open_file_dialog)
        self.addAction('Export PDF', self.export_pdf)
        self.addSeparator()
        self.addAction('Quit', self.quit_application.emit)

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File')
        if fname:
            self.filename = fname[0]
            self.infile_changed.emit(self.filename)

    def export_pdf(self):
        thread = Thread(target=self._export_pdf)
        thread.start()

    def _export_pdf(self):

        # NOTE: in order to avoid system level dependencies, a temporary image (fig.png) of plotly's
        # graph output is referenced in a copy (temp.html) of the current infile. The output .pdf 
        # file is generated from these two temporary files (fig.png and temp.html). 
        if not self.filename:
            self.status_update.emit('Nothing to export')
            return

        if os.path.exists('./temp'):
            shutil.rmtree('./temp')

        fname = self.filename.split('/')[-1].replace('.html', '')
        self.status_update.emit(f'Exporting {fname}.pdf...')
        os.mkdir('temp')
        self.export_requested.emit('fig.png')
        temphtml = './temp/temp.html'
        shutil.copyfile(self.filename, temphtml)
        with open(temphtml, 'r+') as file:
            txt = file.read()
            soup = BeautifulSoup(txt, features='html5lib')
            fig = soup.new_tag('img', type="image/png", src='fig.png') 
            battlegraph_header = soup.new_tag('h3')
            battlegraph_header.insert(1, "Battlegraph Output")
            soup.body.append(battlegraph_header)
            soup.body.append(fig)
            file.write(str(soup))

        pdf = weasyprint.HTML(temphtml).write_pdf()
        open(f'{fname}.pdf', 'wb').write(pdf)
        # shutil.rmtree('./temp')
        self.status_update.emit('Export complete')
        time.sleep(3)
        self.status_update.emit('')


class ShareMenu(QMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(title='Share', *args, **kwargs)


class MainMenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(30)

        self.file_submenu = FileMenu()
        self.share_submenu = ShareMenu()

        self.addMenu(self.file_submenu)
        self.addMenu(self.share_submenu)
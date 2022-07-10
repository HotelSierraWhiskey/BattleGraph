from qtstrap import *
import os
import shutil
from bs4 import BeautifulSoup
import weasyprint


class FileMenu(QMenu):

    infile_changed = Signal(str)
    quit_application = Signal()
    export_requested = Signal(str)

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
        os.mkdir('temp')
        self.export_requested.emit('fig.png')
        temphtml = './temp/temp.html'
        shutil.copyfile(self.filename, temphtml)
        with open(temphtml, 'r+') as file:
            txt = file.read()
            soup = BeautifulSoup(txt, features='html5lib')
            fig = soup.new_tag('img', type="image/png", src='./fig.png')
            battlegraph_header = soup.new_tag('h3')
            battlegraph_header.insert(1, "Battlegraph Output")
            soup.body.append(battlegraph_header)
            soup.body.append(fig)
            file.write(str(soup))

        fname = self.filename.split('/')[-1].replace('.html', '')
        pdf = weasyprint.HTML(temphtml).write_pdf()
        open(f'{fname}.pdf', 'wb').write(pdf)
        shutil.rmtree('./temp')



class MainMenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.file_submenu = FileMenu()

        self.addMenu(self.file_submenu)
from bs4 import BeautifulSoup
from qtstrap import *
from menu import MainMenuBar


class MainWindow(BaseMainWindow):
    def __init__(self, quit_application_callback, parent=None):
        super().__init__(parent=parent)

        self.quit = quit_application_callback

        self.setAcceptDrops(True)
        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.current_file_label = QLabel('')

        main_menu_callbacks = {
            'quit_application_callback': self.quit,
            'change_current_file_label_callback': self.current_file_label.setText
        }

        self.main_menu = MainMenuBar(main_menu_callbacks)

        with CVBoxLayout(widget) as layout:
            with layout.hbox() as layout:
                with layout.vbox() as layout:
                    layout.add(self.main_menu)
                    layout.add(self.current_file_label)


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
            self.current_file_label.setText(fname)
    







# parser = argparse.ArgumentParser(description="process a BattleScribe html file")

# parser.add_argument('infile', type=str, help="provide an html file to process")

# args = parser.parse_args()


# with open(args.infile) as file:
#     soup = BeautifulSoup(file, 'html.parser')

#     title = soup.find('h1')

#     print(title)


# class BattleGraph:
#     def __init__(self):
#         self.data = {}
#         try:
#             with open(args.infile) as file:
#                 soup = BeautifulSoup(file, 'html.parser')
#                 categories = soup.find_all('li', {'class': 'category'})



#                 self.data['title'] = soup.find('h1').contents[0]
#                 self.data['categories'] = [soup.find('h3') for _ in categories]


#         except FileNotFoundError:
#             print(f'File not found ({args.infile})')

#         print(self.data)

# graph = BattleGraph()



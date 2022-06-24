from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.infile = None
        self.soup = None
        self.data = {}
        if self.infile:
            self.load_html()

    def load_html(self):
        with open(self.infile) as file:
            self.soup = BeautifulSoup(file, 'html.parser')


    
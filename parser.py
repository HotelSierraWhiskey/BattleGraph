from __future__ import annotations
from bs4 import BeautifulSoup
    

class Parser:
    def __init__(self, func=None, infile=None):
        self.infile = infile
        self.soup = None
        self.data = {}
        self.parse = func

    def load_html(self):
        try:
            with open(self.infile) as file:
                self.soup = BeautifulSoup(file, 'html.parser')
                self.data = self.parse(self.soup)
        except Exception as e:
            print(e)



# from piechart import parse
# parser = Parser(parse)

# parser.parse()
# parser.infile = './tests/Multidetachment test.html'
# parser.load_html()
# parser.parse_data()

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, infile=None):
        self.infile = infile
        self.soup = None
        self.data = {}
        if self.infile:
            self.load_html()

    def load_html(self):
        with open(self.infile) as file:
            self.soup = BeautifulSoup(file, 'html.parser')
            self.parse_data()

    def parse_data(self):
        self.data['title'] = self.soup.find('h1')
        list_tags = [i for i in self.soup.find_all('li', class_='category')]
        self.data['categories'] = {}

        for i in list_tags:
            entry = str(i.h3.text)
            if 'pts' in entry:
                entry = entry.replace('[', '').replace(']', '')
                entry = entry.split(' ')

                pts = int(entry[-1].replace('pts', ''))
                PL = int(entry[-3])
                slot = ''.join([i + ' ' for i in entry[:-3]]) if len(entry[:-3]) >= 2 else ''.join(entry[:-3])

                self.data['categories'][slot] = pts
                


                
                    



# parser = Parser()
# parser.infile = './tests/test.html'
# parser.load_html()
# parser.parse_data()

# print(parser.data)
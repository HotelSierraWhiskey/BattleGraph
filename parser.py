from __future__ import annotations
from bs4 import BeautifulSoup
from collections import Counter


class Parser:
    def __init__(self, infile=None):
        self.infile = infile
        self.soup = None
        self.data = {}

    def load_html(self):
        with open(self.infile) as file:
            self.soup = BeautifulSoup(file, 'html.parser')
            self._parse()

    def _parse(self):
        self.data['title'] = str(self.soup.find('h1').contents[0])
        list_tags = [i for i in self.soup.find_all('li', class_='category')]
        self.data['categories'] = {}

        for tag in list_tags:
            self._get_slot_pts(tag)

        for slot in self.data['categories'].keys():
            counter = Counter(self.data['categories'][slot]['units'])

            annotation = ''
            for k, v in counter.items():
                annotation += k + ' '
                annotation += 'x' + str(v) + '<br>'

            self.data['categories'][slot]['units'] = annotation[:-4]
        


        
                
    def _get_slot_pts(self, tag):
        entry = tag.h3.text
        units = [t.h4.contents[0] for t in tag.find_all('li', {'class': 'rootselection'})]

        if 'pts' in entry:
            entry = entry.replace('[', '').replace(']', '')
            entry = entry.split(' ')

            pts = int(entry[-1].replace('pts', ''))
            # PL = int(entry[-3])
            slot = ''.join([i + ' ' for i in entry[:-3]]) if len(entry[:-3]) >= 2 else ''.join(entry[:-3])

            if not slot in self.data['categories']:
                self.data['categories'][slot] = {}
                self.data['categories'][slot]['pts'] = pts
                self.data['categories'][slot]['units'] = units

            else:
                self.data['categories'][slot]['pts'] += pts
                for unit in units:
                    self.data['categories'][slot]['units'].append(unit)

        


            # count = self.data['categories'][slot]['units'].count()



    
                    



# parser = Parser()
# parser.infile = './tests/Multidetachment test.html'
# parser.load_html()
# parser.parse_data()

# # print(parser.data['categories'])


# print([parser.data['categories'][i]['units'] for i in parser.data['categories'].keys()])
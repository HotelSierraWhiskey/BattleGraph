import re
from collections import Counter


def parse(soup):
    data = {}
    data['title'] = str(soup.find('h1').text).replace('\n', '')
    list_tags = [i for i in soup.find_all('li', class_='category')]
    data['categories'] = {}

    for tag in list_tags:
        entry = tag.h3.text
        units = [t.h4.contents[0] for t in tag.find_all('li', {'class': 'rootselection'})]

        if 'pts' in entry:
            entry = re.sub('\[|\]', '', entry)
            entry = entry.split(' ')

            pts = int(entry[-1].replace('pts', ''))
            slot = ''.join([i + ' ' for i in entry[:-3]]) if len(entry[:-3]) >= 2 else ''.join(entry[:-3])

            if not slot in data['categories']:
                data['categories'][slot] = {}
                data['categories'][slot]['pts'] = pts
                data['categories'][slot]['units'] = units

            else:
                data['categories'][slot]['pts'] += pts
                for unit in units:
                    data['categories'][slot]['units'].append(unit)
    
    unit_names = set()

    for slot in data['categories'].keys():
        counter = Counter(data['categories'][slot]['units'])

        annotation = ''
        for k, v in counter.items():
            annotation += k + ' '
            annotation += 'x' + str(v) + '<br>'
            # unit_names.add(k.split(' [')[0])

        data['categories'][slot]['units'] = annotation[:-4] + '<br><b>total: ' + str(data['categories'][slot]['pts'])   # remove trailing linebreak

    profiles = soup.find_all('td', {'class': 'profile-name'})

    labels = list(data['categories'].keys())
    values = []
    text = []
    for label in labels:

        values.append(data['categories'][label]['pts'])
        text.append(data['categories'][label]['units'])

    title = data['title']


    # print(profiles)

    return {'labels': labels, 'values': values, 'text': text, 'title': title}
            
    
    

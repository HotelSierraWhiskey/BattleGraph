from collections import Counter


def parse(soup):
    data = {}
    data['title'] = str(soup.find('h1').contents[0])
    list_tags = [i for i in soup.find_all('li', class_='category')]
    data['categories'] = {}

    for tag in list_tags:
        entry = tag.h3.text
        units = [t.h4.contents[0] for t in tag.find_all('li', {'class': 'rootselection'})]

        if 'pts' in entry:
            entry = entry.replace('[', '').replace(']', '')
            entry = entry.split(' ')

            pts = int(entry[-1].replace('pts', ''))
            # PL = int(entry[-3])
            slot = ''.join([i + ' ' for i in entry[:-3]]) if len(entry[:-3]) >= 2 else ''.join(entry[:-3])

            if not slot in data['categories']:
                data['categories'][slot] = {}
                data['categories'][slot]['pts'] = pts
                data['categories'][slot]['units'] = units

            else:
                data['categories'][slot]['pts'] += pts
                for unit in units:
                    data['categories'][slot]['units'].append(unit)
    
    for slot in data['categories'].keys():
        counter = Counter(data['categories'][slot]['units'])

        annotation = ''
        for k, v in counter.items():
            annotation += k + ' '
            annotation += 'x' + str(v) + '<br>'

        data['categories'][slot]['units'] = annotation[:-4]    # remove trailing linebreak

    return data
            
    
    
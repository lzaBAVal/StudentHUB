'''

    This function takes url of the form - 'https://aues.arhit.kz/rasp/scheduleNew.php?sg=1734&schedule=32'

'''

from bs4 import BeautifulSoup
from requests import get


def search_group(url: str):

    groups_dict = {}
    resp = get(url)
    soup = BeautifulSoup(resp.text, 'lxml')


    for opt in soup.find_all('option'):
        groups_dict.setdefault(str(opt.string).lower().strip(), opt['value'])
    groups_dict.pop('- группа -')

    groups_keys = []
    groups_values = []
    for key in groups_dict.keys():
        groups_keys.append(key)

    for value in groups_dict.values():
        groups_values.append(value)

    #print(groups_keys)
    #print(groups_values)

    groups_keys = groups_keys[:groups_keys.index('- преподаватель -')]
    groups_values = groups_values[:len(groups_keys)]
    groups_dict = {}

    for i in range(len(groups_keys) - 1):
        groups_dict.setdefault(groups_keys[i-1], groups_values[i-1])

    return groups_dict


#print(search_group('https://aues.arhit.kz/rasp/start_ext.php'))
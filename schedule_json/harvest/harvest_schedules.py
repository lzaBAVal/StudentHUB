'''

    This function takes url of the form

'''

import re
import requests
from bs4 import BeautifulSoup

days = {
    'monday': 'понедельник',
    'tuesday': 'вторник',
    'wednesday': 'среда',
    'thursday': 'четверг',
    'friday': 'пятница',
    'saturday': 'суббота'
}


def search_schedule(url: str):
    '''
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(pgsql_conn(get_group_value( \
            dict(loop.run_until_complete(pgsql_conn(get_group_name(1)))[0])['group_name'])))

        print(response)
    '''
    resp = requests.get(url)
    shed = BeautifulSoup(resp.text, 'lxml')

    matrix = []
    shed_dict = {}

    for th in shed.find_all('th'):
        matrix.append(th.string)
    for td in shed.find_all('td'):
        tmp_composer = []
        for i in td:
            if not re.match(r'<br/>', str(i)) and i != '\n' and i != ' ':
                tmp_composer.append(str(i).strip())
        matrix.append(" ".join(tmp_composer))

    for i in range(len(matrix)):
        flag = 0
        current_day = matrix[i].lower()
        if current_day in list(days.values()):
            for j in range(i, len(matrix), 6):
                order = int(re.search(r'\d{1,2}', re.search(r'\[.*\]', matrix[j + 1]).group()).group())
                current_day_j = list(days.keys())[list(days.values()).index(current_day)]
                tmp_dict = {
                    current_day_j: {
                        order: {
                            'time': re.search(r'\d{1,2}[.:]\d{2}[- ]*\d{1,2}[.:]\d{2}', matrix[j + 1]).group(),
                            'subgroup': re.search(r'.*', matrix[j + 2]).group(),
                            'lesson': re.search(r'.*', matrix[j + 3]).group(),
                            'teacher': re.search(r'.*', matrix[j + 4]).group(),
                            'classroom': re.search(r'.*', matrix[j + 5]).group()
                        }
                    }
                }
                if matrix[j].lower() != current_day and matrix[j].lower() != '':
                    break
                elif flag == 0:
                    shed_dict.setdefault(current_day_j, [tmp_dict[current_day_j]])
                    flag = 1
                else:
                    shed_dict[current_day_j].append(tmp_dict[current_day_j])

    return shed_dict

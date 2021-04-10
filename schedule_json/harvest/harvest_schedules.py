'''

    This function takes url of the form

'''

import re
import requests
import time as tm

from bs4 import BeautifulSoup

from schedule_json.output.get_schedule_object import check_sched
from vars import days, Time, Day_of_week, Lesson, Sched
from logs.scripts.logging_core import init_logger


logger = init_logger()


def search_schedule(url: str):

    resp = requests.get(url)
    tm.sleep(.5)
    shed = BeautifulSoup(resp.text, 'lxml')

    matrix = []
    sched_json = {}

    for th in shed.find_all('th'):
        matrix.append(th.string)
    for td in shed.find_all('td'):
        tmp_composer = []
        for i in td:
            if not re.match(r'<br/>', str(i)) and i != '\n' and i != ' ':
                tmp_composer.append(str(i).strip())
        matrix.append(" ".join(tmp_composer))

    if len(matrix) <= 6:
        return -1

    for i in range(len(matrix)):
        current_day = matrix[i].lower()

        if current_day in list(days.values()):
            lessons = []
            for j in range(i, len(matrix), 6):
                get_time = re.findall(r'(\d{1,2})[.:](\d{2})[- ]*(\d{1,2})[.:](\d{2})', matrix[j + 1])[0]
                time = {
                    "start": str(get_time[0] + ':' + get_time[1]),
                    "end": str(get_time[2] + ':' + get_time[3])
                }
                time = Time(**time)

                lesson = {
                    'time': time,
                    'subgroup': str(re.search(r'.*', matrix[j + 2]).group()),
                    'lesson': str(re.search(r'.*', matrix[j + 3]).group()),
                    'teacher': str(re.search(r'.*', matrix[j + 4]).group()),
                    'classroom': str(re.search(r'.*', matrix[j + 5]).group())
                }
                lesson = Lesson(**lesson)
                if matrix[j].lower() != current_day and matrix[j].lower() != '':
                    day = {
                        "lessons": lessons
                    }
                    day_o = Day_of_week(**day)
                    sched_json.setdefault(list(days.keys())[list(days.values()).index(current_day)], day_o)
                else:
                    lessons.append(lesson)
                    if len(matrix) - j < 7:
                        day = {
                            "lessons": lessons
                        }
                        day_o = Day_of_week(**day)
                        sched_json.setdefault(list(days.keys())[list(days.values()).index(current_day)], day_o)
    if check_sched(sched_json) is False:
        return -1
    sched_dict = Sched.parse_obj(sched_json)
    sched_dict = sched_dict.dict()
    return sched_dict

import re, asyncio, json, requests

from typing import Optional
from pydantic import BaseModel
from bs4 import BeautifulSoup

days = {
    'monday': 'понедельник',
    'tuesday': 'вторник',
    'wednesday': 'среда',
    'thursday': 'четверг',
    'friday': 'пятница',
    'saturday': 'суббота'
}

class Time(BaseModel):
    start: str
    end: str

class Lesson(BaseModel):
    time: Time
    subgroup: str
    lesson: str
    teacher: str
    classroom: str

class Day_of_week(BaseModel):
    lessons: list[Lesson]

class Sched(BaseModel):
    monday: Optional[Day_of_week]
    tuesday: Optional[Day_of_week]
    wednesday: Optional[Day_of_week]
    thursday: Optional[Day_of_week]
    friday: Optional[Day_of_week]
    saturday: Optional[Day_of_week]


def search_schedule(url: str = 'https://aues.arhit.kz/rasp/scheduleNew.php?sg=2017&schedule=32'):

    resp = requests.get(url)
    shed = BeautifulSoup(resp.text, 'lxml')

    matrix = []
    shed_json = {}

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
                print(lesson)
                print(j)
                if matrix[j].lower() != current_day and matrix[j].lower() != '':
                    day = {
                        "lessons": lessons
                    }
                    day_o = Day_of_week(**day)
                    shed_json.setdefault(list(days.keys())[list(days.values()).index(current_day)], day_o)
                    print(current_day + ' ' + str(lesson))
                else:
                    lessons.append(lesson)
                    print(current_day + ' ' + str(lesson))
                    if len(matrix) - j < 7:
                        day = {
                            "lessons": lessons
                        }
                        day_o = Day_of_week(**day)
                        shed_json.setdefault(list(days.keys())[list(days.values()).index(current_day)], day_o)

    shed_json = Sched(**shed_json)
    return shed_json

sched = search_schedule()
print(len(sched.dict()['tuesday']['lessons'])) # 2
print(sched.json())
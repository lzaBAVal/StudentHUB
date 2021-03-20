from datetime import datetime, time
from schedule.output.type_of_sched import WeekDays_EN
from pydantic import BaseModel
from typing import Optional

import re


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

# ----------------------------------------------------------------------------------------------------

first_lesson = time(hour=8, minute=40)
last_lesson = time(hour=18, minute=40)

json = '''{"monday": null, "tuesday": {"lessons": [{"time": {"start": "17:40", "end": "18:20"}, "subgroup": "", "lesson": "\u0424\u041a \u043f\u0440\u0430\u043a.", "teacher": "\u0415\u0440\u043c\u043e\u043b\u0430\u0435\u0432 \u041a. \u0412. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "18:40", "end": "19:20"}, "subgroup": "", "lesson": "\u0424\u041a \u043f\u0440\u0430\u043a.", "teacher": "\u0415\u0440\u043c\u043e\u043b\u0430\u0435\u0432 \u041a. \u0412. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "wednesday": {"lessons": [{"time": {"start": "11:40", "end": "12:20"}, "subgroup": "", "lesson": "\u0426\u0421 \u043b\u0435\u043a.", "teacher": "\u0411\u0435\u0440\u0434\u0438\u0431\u0430\u0435\u0432 \u0420. \u0428. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "12:40", "end": "13:20"}, "subgroup": "", "lesson": "\u0422\u0412\u0418\u041c\u0421 \u043f\u0440\u0430\u043a.", "teacher": "\u041c\u0430\u0441\u0430\u043d\u043e\u0432\u0430 \u0410. \u0416. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "14:40", "end": "15:20"}, "subgroup": "", "lesson": "\u041c\u0421\u041f\u0417\u041a\u041f \u043f\u0440\u0430\u043a.", "teacher": "\u0410\u0431\u0440\u0430\u0445\u043c\u0430\u0442\u043e\u0432\u0430 \u0413. \u0410. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "thursday": {"lessons": [{"time": {"start": "09:40", "end": "10:20"}, "subgroup": "1", "lesson": "\u0426\u0421 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "10:40", "end": "11:20"}, "subgroup": "1", "lesson": "\u0426\u0421 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "11:40", "end": "12:20"}, "subgroup": "", "lesson": "\u0422\u0417\u041a\u0418 \u043b\u0435\u043a.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "14:40", "end": "15:20"}, "subgroup": "", "lesson": "\u0411\u041e\u0421 \u043b\u0435\u043a.", "teacher": "\u0421\u0430\u0442\u0438\u043c\u043e\u0432\u0430 \u0415. \u0413. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "friday": {"lessons": [{"time": {"start": "09:40", "end": "10:20"}, "subgroup": "1", "lesson": "\u0422\u0417\u041a\u0418 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "10:40", "end": "11:20"}, "subgroup": "1", "lesson": "\u0422\u0417\u041a\u0418 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "11:40", "end": "12:20"}, "subgroup": "", "lesson": "\u0422\u0412\u0418\u041c\u0421 \u043b\u0435\u043a.", "teacher": "\u041c\u0430\u0441\u0430\u043d\u043e\u0432\u0430 \u0410. \u0416. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "saturday": {"lessons": [{"time": {"start": "09:40", "end": "10:20"}, "subgroup": "1", "lesson": "\u0411\u041e\u0421 \u043b\u0430\u0431.", "teacher": "\u0417\u0438\u043c\u0438\u043d \u0418.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "10:40", "end": "11:20"}, "subgroup": "1", "lesson": "\u0411\u041e\u0421 \u043b\u0430\u0431.", "teacher": "\u0417\u0438\u043c\u0438\u043d \u0418.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}}'''

def get_free_time(group_sched=None):

    free_time = []
    sched: dict = Sched.parse_raw(json).dict()
    print(sched)


    for day in sched:
        if sched[day] == None:
            print(f"On {day} there is free time - all")
        start, end = [], []
        free_time = []
        for i in range(len(sched[day]['lessons'])):
            start.append(datetime.strptime(str(sched[day]['lessons'][i]['time']['start']), "%H:%M").time())
            end.append(datetime.strptime(str(sched[day]['lessons'][i]['time']['end']), "%H:%M"))

        for t in range(13):
            t_lesson = time(hour=first_lesson.hour + 1 * t, minute=first_lesson.minute)
            #t_lesson = time.strftime(t_lesson, '%H:%M')
            if t_lesson not in start:
                free_time.append(t_lesson)
        print(f"On {day} there is free time - {len(free_time)}")


def add_lesson(day: int = None, time_start: str = None, time_end: str = None, name_lesson: str = None, teacher: str = None, subgroup: int = None, classroom: str = None):
    if day < 1 or day > 6:
        try:
            raise ValueError('Not valid day!')
        except ValueError:
            print('The day number must be between one and six')
            print('DAY VALUE: ' + str(day))
            return -1
    else:
        day -= 1

    if subgroup == None:
        pass
    elif (subgroup < 0 or subgroup > 3):
        try:
            raise ValueError('ERROR: Not valid sub_group!')
        except ValueError:
            print('ERROR SUB_GROUP: ' + str(subgroup))
            return -1
    else:
        try:
            raise ValueError('ERROR: Not valid type sub_group!')
        except ValueError:
            print('ERROR SUB_GROUP: ' + str(subgroup))
            return -1

    if re.search(r"[\.\<\>\(\)\{\}\]]", name_lesson) or len(name_lesson) > 30:
        try:
            raise ValueError('ERROR: Not valid name_lesson!')
        except ValueError:
            print('ERROR NAME_LESSON: ' + str(name_lesson))
            return -1

    day = WeekDays_EN[day]
    sched: dict = Sched.parse_raw(json).dict()

    time = {
        "start": time_start,
        "end": time_end
    }
    time = Time(**time)

    lesson = {
        'time': time,
        'subgroup': str(subgroup),
        'lesson': name_lesson,
        'teacher': teacher,
        'classroom': classroom
    }
    lesson = Lesson(**lesson)

    if sched[day] != None:
        for l in sched[day]['lessons']:
            l = l['time']['start']
            if l == time_start:
                return -1
        sched[day]['lessons'].append(lesson)
    else:
        sched[day] = {'lessons': [lesson]}
        print(sched[day])

    sched = Sched(**sched)
    print(sched.json())
    return sched


add_lesson(day=3, time_start='12:40', time_end="13:20", name_lesson='test_lesson', teacher='Василиса', classroom='Онлайн')
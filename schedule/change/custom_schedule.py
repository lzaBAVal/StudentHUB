from schedule.output.get_schedule_object import get_sched_list
from datetime import datetime, time
from schedule.output.type_of_sched import WeekDays_EN

import asyncio, re

# ----------------------------------------------------------------------------------------------------

first_lesson = time(hour=8, minute=40)
last_lesson = time(hour=18, minute=40)

def get_free_time(group_sched=None):
    group_sched = asyncio.get_event_loop().run_until_complete(get_sched_list(690976128))
    free_time = []

    for day in group_sched:
        lesson: dict
        day_sched_time = []
        day_sched_str = []
        for lesson in group_sched[day]:
            time_day = list(re.findall(r'(\d{1,2}).{0,3}(\d{2}).{0,3}(\d{1,2}).{0,3}(\d{2})', list(lesson.values())[0]['time'])[0])
            time_day = [":".join(time_day[t+0:t+2]) for t in range(0, 4, 2)]
            day_sched_str.append(time_day[0])

            res = datetime.strptime(time_day[0], "%H:%M")
            day_sched_time.append(res)

        for t in range(13):
            t_lesson = time(hour=first_lesson.hour + 1 * t, minute=first_lesson.minute)
            t_lesson = time.strftime(t_lesson, '%H:%M')
            if t_lesson not in day_sched_str:
                free_time.append(t_lesson)

    return free_time


def add_lesson(day: int = None, time_lesson: str = None, name_lesson: str = None, teacher: str = None, sub_group: int = None, classroom: str = None):

    if day < 0 or day > 8:
        try:
            raise ValueError('Not valid day!')
        except ValueError:
            print('The day number must be between one and seven')
            print('DAY VALUE: ' + str(day))
            return -1

    if sub_group == None:
        pass
    elif (sub_group < 0 or sub_group > 3):
        try:
            raise ValueError('ERROR: Not valid sub_group!')
        except ValueError:
            print('ERROR SUB_GROUP: ' + str(sub_group))
            return -1
    else:
        try:
            raise ValueError('ERROR: Not valid type sub_group!')
        except ValueError:
            print('ERROR SUB_GROUP: ' + str(sub_group))
            return -1

    if re.search(r'[\.\<\>\(\)\{\}\]]', name_lesson) or len(name_lesson) > 30:
        try:
            raise ValueError('ERROR: Not valid name_lesson!')
        except ValueError:
            print('ERROR NAME_LESSON: ' + str(name_lesson))
            return -1

    group_sched = asyncio.get_event_loop().run_until_complete(get_sched_list(690976128))
    lesson = {}
    lesson.setdefault(0, {'time': time_lesson, 'sub_group': sub_group, 'lesson': name_lesson, 'teacher': teacher, 'classroom': classroom})
    print(lesson)
    group_sched[WeekDays_EN[day]].append(lesson)
    print(group_sched[WeekDays_EN[day]])
    return group_sched

print(add_lesson(day=1 ,time_lesson='9:40 - 10:20', name_lesson='test_lesson', teacher='Василиса', classroom='Онлайн'))
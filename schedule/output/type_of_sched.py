"""

    schedule_for_today принимает словар shed_dict и отдает строку, в которой содержится расписание для вывода клиенту

"""

import datetime as dt
import re

WeekDays_RU = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')
WeekDays_EN = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

now = dt.datetime.now()
weekday = now.isoweekday() - 1
day = WeekDays_EN[weekday]


def schedule_for_today(sched, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):
    todays_shed = sched[day]

    result = '-------------------' + '\n' + str(WeekDays_RU[weekday]).title() + '\n' + '-------------------'
    for i in todays_shed:
        for k, v in i.items():
            if time:
                result += '\n' + 'Время: ' + i[k]['time']
            if subgroup:
                result += '\n' + 'Подгруппа: ' + i[k]['subgroup']
            if lesson:
                result += '\n' + 'Предмет: ' + i[k]['lesson']
            if teacher:
                result += '\n' + 'Преподаватель: ' + i[k]['teacher']
            if classroom:
                result += '\n' + 'Аудитория: ' + i[k]['classroom']
            result = result + '\n' + '-------------------'
            result = ''.join(result)

    return result


def all_schedule(sched, time=True, subgroup=False, lesson=True, teacher=False, classroom=False):
    result = ''
    for k, v in sched.items():
        result += '\n' + str(WeekDays_RU[WeekDays_EN.index(k)]).title() + '\n' + '-------------------'
        for i in v:
            for k1, v1 in i.items():
                if time:
                    result += '\n' + 'Время: ' + i[k1]['time']
                if subgroup:
                    result += '\n' + 'Подгруппа: ' + i[k1]['subgroup']
                if lesson:
                    result += '\n' + 'Предмет: ' + i[k1]['lesson']
                if teacher:
                    result += '\n' + 'Преподаватель: ' + i[k1]['teacher']
                if classroom:
                    result += '\n' + 'Аудитория: ' + i[k1]['classroom']
                result = result + '\n'
                result = ''.join(result)

    return result


def current_lesson(sched, time=True, subgroup=True, lesson=True, teacher=True, classroom=True):
    result, delta = None, None
    todays_sched = sched[day]
    current_time = now.strptime(now.strftime('%H:%M'), '%H:%M')
    amount_lessons = len(todays_sched)
    counter_lessons = 0
    end = 0

    for i in todays_sched:
        for k, v in i.items():
            counter_lessons += 1
            tmp_time = now.strptime(re.search(r'\d{2}:\d{2}', i[k]['time']).group(), '%H:%M')
            delta = tmp_time - current_time
            if not re.match(r'^-', str(delta)):
                # До начала пары (delta.seconds//60) минут
                end = 1
                break
            elif counter_lessons == amount_lessons:
                # Пары уже закончились
                result = 'Пары уже закончились!'
                return result
        if end == 1:
            break

    future_lesson = todays_sched[counter_lessons - 1]

    for k, v in future_lesson.items():
        result = 'Следующая пара наченется через ' + str(delta.seconds // 60) + ' минуты'
        if time:
            result += '\n' + 'Время: ' + future_lesson[k]['time']
        if subgroup:
            result += '\n' + 'Подгруппа: ' + future_lesson[k]['subgroup']
        if lesson:
            result += '\n' + 'Предмет: ' + future_lesson[k]['lesson']
        if teacher:
            result += '\n' + 'Преподаватель: ' + future_lesson[k]['teacher']
        if classroom:
            result += '\n' + 'Аудитория: ' + future_lesson[k]['classroom']
        result = result + '\n' + '-------------------'
        result = ''.join(result)

    return result

"""

    schedule_for_today принимает словар shed_dict и отдает строку, в которой содержится расписание для вывода клиенту

"""

import datetime as dt
import re

from vars import WeekDays_EN, WeekDays_RU


def construct_lesson(future_lesson, result, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):
    if lesson:
        result += '\nПредмет: ' + str(future_lesson['lesson'])
    if time:
        result += '\nВремя: ' + str(future_lesson['time']['start'] + ' - ' + str(future_lesson['time']['end']))
    if subgroup:
        result += '\nПодгруппа: ' + str(future_lesson['subgroup'])
    if teacher:
        result += '\nПреподаватель: ' + str(future_lesson['teacher'])
    if classroom:
        result += '\nАудитория: ' + str(future_lesson['classroom'])
        
    return result


def schedule_for_today(sched, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Сегодня выходной'
    todays_shed = sched[day]
    result = '-------------------\n' + str(WeekDays_RU[weekday]).title() + '\n-------------------\n'
    if todays_shed is None:
        result += 'Нет занятий'
    else:
        for i in todays_shed['lessons']:
            result = construct_lesson(i, result, time, subgroup, lesson, teacher, classroom)
            result += '-------------------\n'
    result = ''.join(result)
    return result


def schedule_for_tommorow(sched, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):
    now = dt.datetime.now()
    weekday = now.isoweekday()
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Завтра выходной'
    todays_shed = sched[day]
    result = '-------------------\n' + str(WeekDays_RU[weekday]).title() + '\n-------------------\n'
    if todays_shed is None:
        result += 'Нет занятий'
    else:
        for i in todays_shed['lessons']:
            result = construct_lesson(i, result, time, subgroup, lesson, teacher, classroom)
            result += '-------------------\n'
    result = ''.join(result)

    return result


def all_schedule(sched, time=True, subgroup=False, lesson=True, teacher=False, classroom=False):
    result = ''
    for k in sched:
        result += str(WeekDays_RU[WeekDays_EN.index(k)]).title() + '\n-------------------\n'
        if sched[k] is None:
            result += 'Нет занятий\n\n'
            continue
        for i in sched[k]['lessons']:
            result = construct_lesson(i, result, time, subgroup, lesson, teacher, classroom)
            result = ''.join(result) + '\n'

    return result


def current_lesson(sched, time=True, subgroup=True, lesson=True, teacher=True, classroom=True):
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Сегодня выходной'
    if sched[day] is None:
        return -1, 'Сегодня нет занятий'
    result, delta = None, None
    today_sched = sched[day]
    current_time = now.strptime(now.strftime('%H:%M'), '%H:%M')
    amount_lessons = len(today_sched['lessons'])
    counter_lessons = 0
    end = 0

    for i in today_sched['lessons']:
        counter_lessons += 1
        tmp_time = now.strptime(re.search(r'\d{1,2}:\d{2}', str(i['time']['start'])).group(), '%H:%M')
        delta = tmp_time - current_time
        if not re.match(r'^-', str(delta)):
            end = 1
            break
        elif counter_lessons == amount_lessons:
            result = 'Пары уже закончились!'
            return result
        if end == 1:
            break

    future_lesson = today_sched['lessons'][counter_lessons - 1]
    result = 'Следующая пара наченется через ' + str(delta.seconds // 60) + ' минуты'
    result = construct_lesson(future_lesson, result, time, subgroup, lesson, teacher, classroom)

    return result

"""

    schedule_for_today принимает словар shed_dict и отдает строку, в которой содержится расписание для вывода клиенту

"""

import datetime as dt
import re

from vars import WeekDays_EN, WeekDays_RU


def construct_lesson(future_lesson, result, **parts):
    if parts['lesson']:
        result += '\nПредмет: ' + str(future_lesson['lesson'])
    if parts['time']:
        result += '\nВремя: ' + str(future_lesson['time']['start'] + ' - ' + str(future_lesson['time']['end']))
    if parts['subgroup']:
        result += '\nПодгруппа: ' + str(future_lesson['subgroup'])
    if parts['teacher']:
        result += '\nПреподаватель: ' + str(future_lesson['teacher'])
    if parts['classroom']:
        result += '\nАудитория: ' + str(future_lesson['classroom'])
        
    return result


def schedule_for_today(sched, parts):
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Сегодня выходной'
    todays_shed = sched[day]
    result = '-------------------\n' + str(WeekDays_RU[weekday]).title() + '\n-------------------'
    if todays_shed is None or len(todays_shed['lessons']) == 0:
        result += 'Нет занятий'
    else:
        for i in todays_shed['lessons']:
            result = construct_lesson(i, result, **parts)
            result += '\n-------------------\n'
    result = ''.join(result)
    return result


def schedule_for_tommorow(sched, parts):
    now = dt.datetime.now()
    weekday = now.isoweekday()
    if weekday == 7:
        weekday = 0
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Завтра выходной'
    todays_shed = sched[day]
    result = '-------------------\n' + str(WeekDays_RU[weekday]).title() + '\n-------------------\n'
    if todays_shed is None:
        result += 'Нет занятий'
    else:
        for i in todays_shed['lessons']:
            result = construct_lesson(i, result, **parts)
            result += '\n-------------------\n'
    result = ''.join(result)

    return result


def all_schedule(sched, **parts):
    result = ''
    for k in sched:
        result += '\n' + str(WeekDays_RU[WeekDays_EN.index(k)]).title() + '\n-------------------'
        if sched[k] is None:
            result += '\nНет занятий\n\n'
            continue
        for i in sched[k]['lessons']:
            result = construct_lesson(i, result, **parts)
            result = ''.join(result) + '\n'

    return result


def current_lesson(sched, parts):
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

    if len(today_sched['lessons']) == 0:
        result = 'Сегодня нет пар!'
        return result

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
    result = construct_lesson(future_lesson, result, **parts)

    return result

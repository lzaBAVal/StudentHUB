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
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Сегодня выходной'
    todays_shed = sched[day]
    result = '-------------------' + '\n' + str(WeekDays_RU[weekday]).title() + '\n' + '-------------------' + '\n'
    if todays_shed is None:
        result += 'Нет занятий'
    else:
        for i in todays_shed['lessons']:
            if lesson:
                result += 'Предмет: ' + i['lesson'] + '\n'
            if time:
                result += 'Время: ' + i['time']['start'] + ' - ' + i['time']['end'] + '\n'
            if subgroup:
                result += 'Подгруппа: ' + i['subgroup'] + '\n'
            if teacher:
                result += 'Преподаватель: ' + i['teacher'] + '\n'
            if classroom:
                result += 'Аудитория: ' + i['classroom'] + '\n'
            result += '-------------------' + '\n'
    result = ''.join(result)
    return result


def schedule_for_tommorow(sched, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):
    now = dt.datetime.now()
    weekday = now.isoweekday()
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Сегодня выходной'
    todays_shed = sched[day]
    result = '-------------------' + '\n' + str(WeekDays_RU[weekday]).title() + '\n' + '-------------------' + '\n'
    if todays_shed is None:
        result += 'Нет занятий'
    else:
        for i in todays_shed['lessons']:
            if lesson:
                result += 'Предмет: ' + i['lesson'] + '\n'
            if time:
                result += 'Время: ' + i['time']['start'] + ' - ' + i['time']['end'] + '\n'
            if subgroup:
                result += 'Подгруппа: ' + i['subgroup'] + '\n'
            if teacher:
                result += 'Преподаватель: ' + i['teacher'] + '\n'
            if classroom:
                result += 'Аудитория: ' + i['classroom'] + '\n'
            result += '-------------------' + '\n'
    result = ''.join(result)
    return result


def all_schedule(sched, time=True, subgroup=False, lesson=True, teacher=False, classroom=False):
    result = ''
    for k in sched:
        result += str(WeekDays_RU[WeekDays_EN.index(k)]).title() + '\n' + '-------------------' + '\n'
        if sched[k] is None:
            result += 'Нет занятий' + '\n\n'
            continue
        for i in sched[k]['lessons']:
            if lesson:
                result += 'Предмет: ' + i['lesson'] + '\n'
            if time:
                result += 'Время: ' + i['time']['start'] + ' - ' + i['time']['end'] + '\n'
            if subgroup:
                result += 'Подгруппа: ' + i['subgroup'] + '\n'
            if teacher:
                result += 'Преподаватель: ' + i['teacher'] + '\n'
            if classroom:
                result += 'Аудитория: ' + i['classroom'] + '\n'
            result = ''.join(result) + '\n'

    return result


def current_lesson(sched, time=True, subgroup=True, lesson=True, teacher=True, classroom=True):
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]
    if day == 'sunday':
        return -1, 'Сегодня выходной'
    if sched[day] is None:
        return -1
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
    if lesson:
        result += '\n' + 'Предмет: ' + str(future_lesson['lesson'])
    if time:
        result += '\n' + 'Время: ' + str(future_lesson['time']['start'] + ' - ' + str(future_lesson['time']['end']))
    if subgroup:
        result += '\n' + 'Подгруппа: ' + str(future_lesson['subgroup'])
    if teacher:
        result += '\n' + 'Преподаватель: ' + str(future_lesson['teacher'])
    if classroom:
        result += '\n' + 'Аудитория: ' + str(future_lesson['classroom'])
    result = result
    result = ''.join(result)

    return result

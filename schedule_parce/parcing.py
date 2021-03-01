'''

    schedule_for_today принимает словар shed_dict и отдает строку, в которой содержится расписание на сегодняшний день

'''

import requests
import datetime as dt
import re
import asyncio

from bs4 import BeautifulSoup
from schedule_parce.group_by_days import create_group_days
from DB.pgsql_conn import pgsql_conn
#from DB.pgsql_requests import

WeekDays_RU = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')
WeekDays_EN = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

now = dt.datetime.now()
weekday = now.isoweekday() - 1
day = WeekDays_EN[weekday]

def schedule_for_today(sched, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):

    resp = requests.get(sched)
    soup = BeautifulSoup(resp.text, 'lxml')
    todays_shed = []
    result = ''
    shed_dict = create_group_days(soup)
    todays_shed = shed_dict[day]

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


'''

Почему то все уже рассортировано...

def sort_dicts(dicts):
    result = []
    tmp = []
    for i in dicts:
        for k, v in i.items():
            tmp.append(k)
    print(tmp)
    return True
'''

def all_shedule(sched, time=True, subgroup=False, lesson=True, teacher=False, classroom=False):
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

    todays_shed = sched[day]
    current_time = now.strptime(now.strftime('%H:%M'), '%H:%M')
    amount_lessons = len(todays_shed)
    counter_lessons = 0
    end = 0

    for i in todays_shed:
        biggest_diff = 0
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

    future_lesson = todays_shed[counter_lessons - 1]

    for k, v in future_lesson.items():
        result = 'Следующая пара наченется через ' + str(delta.seconds//60) + ' минуты'
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
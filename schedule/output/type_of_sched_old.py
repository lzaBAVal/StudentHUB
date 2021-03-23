"""

    schedule_for_today принимает словар shed_dict и отдает строку, в которой содержится расписание для вывода клиенту

"""

import datetime as dt
import re, json

from vars import WeekDays_EN, WeekDays_RU

now = dt.datetime.now()
weekday = now.isoweekday() - 1
day = WeekDays_EN[weekday]

json_str = '''{"monday": null, "tuesday": {"lessons": [{"time": {"start": "17:40", "end": "18:20"}, "subgroup": "", "lesson": "\u0424\u041a \u043f\u0440\u0430\u043a.", "teacher": "\u0415\u0440\u043c\u043e\u043b\u0430\u0435\u0432 \u041a. \u0412. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "18:40", "end": "19:20"}, "subgroup": "", "lesson": "\u0424\u041a \u043f\u0440\u0430\u043a.", "teacher": "\u0415\u0440\u043c\u043e\u043b\u0430\u0435\u0432 \u041a. \u0412. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "wednesday": {"lessons": [{"time": {"start": "11:40", "end": "12:20"}, "subgroup": "", "lesson": "\u0426\u0421 \u043b\u0435\u043a.", "teacher": "\u0411\u0435\u0440\u0434\u0438\u0431\u0430\u0435\u0432 \u0420. \u0428. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "12:40", "end": "13:20"}, "subgroup": "", "lesson": "\u0422\u0412\u0418\u041c\u0421 \u043f\u0440\u0430\u043a.", "teacher": "\u041c\u0430\u0441\u0430\u043d\u043e\u0432\u0430 \u0410. \u0416. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "14:40", "end": "15:20"}, "subgroup": "", "lesson": "\u041c\u0421\u041f\u0417\u041a\u041f \u043f\u0440\u0430\u043a.", "teacher": "\u0410\u0431\u0440\u0430\u0445\u043c\u0430\u0442\u043e\u0432\u0430 \u0413. \u0410. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "thursday": {"lessons": [{"time": {"start": "09:40", "end": "10:20"}, "subgroup": "1", "lesson": "\u0426\u0421 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "10:40", "end": "11:20"}, "subgroup": "1", "lesson": "\u0426\u0421 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "11:40", "end": "12:20"}, "subgroup": "", "lesson": "\u0422\u0417\u041a\u0418 \u043b\u0435\u043a.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "14:40", "end": "15:20"}, "subgroup": "", "lesson": "\u0411\u041e\u0421 \u043b\u0435\u043a.", "teacher": "\u0421\u0430\u0442\u0438\u043c\u043e\u0432\u0430 \u0415. \u0413. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "friday": {"lessons": [{"time": {"start": "09:40", "end": "10:20"}, "subgroup": "1", "lesson": "\u0422\u0417\u041a\u0418 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "10:40", "end": "11:20"}, "subgroup": "1", "lesson": "\u0422\u0417\u041a\u0418 \u043b\u0430\u0431.", "teacher": "\u0414\u043c\u0438\u0442\u0440\u0438\u0435\u0432\u0430 \u041c. \u0412. \u0441\u0442. \u043f\u0440\u0435\u043f.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "11:40", "end": "12:20"}, "subgroup": "", "lesson": "\u0422\u0412\u0418\u041c\u0421 \u043b\u0435\u043a.", "teacher": "\u041c\u0430\u0441\u0430\u043d\u043e\u0432\u0430 \u0410. \u0416. \u0434\u043e\u0446.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}, "saturday": {"lessons": [{"time": {"start": "09:40", "end": "10:20"}, "subgroup": "1", "lesson": "\u0411\u041e\u0421 \u043b\u0430\u0431.", "teacher": "\u0417\u0438\u043c\u0438\u043d \u0418.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}, {"time": {"start": "10:40", "end": "11:20"}, "subgroup": "1", "lesson": "\u0411\u041e\u0421 \u043b\u0430\u0431.", "teacher": "\u0417\u0438\u043c\u0438\u043d \u0418.", "classroom": "\u041e\u043d\u043b\u0430\u0439\u043d"}]}}'''


def schedule_for_today(sched, time=True, subgroup=False, lesson=True, teacher=True, classroom=False):
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]

    todays_shed = dict(json.loads(sched))[day]

    result = ''

    result += '-----------------------'
    for i in todays_shed['lessons']:
        if time:
            result += '\n' + 'Время: ' + str(i['time']['start']) + ' - ' + str(i['time']['end'])
        if subgroup:
            result += '\n' + 'Подгруппа: ' + i['subgroup']
        if lesson:
            result += '\n' + 'Предмет: ' + i['lesson']
        if teacher:
            result += '\n' + 'Преподаватель: ' + i['teacher']
        if classroom:
            result += '\n' + 'Аудитория: ' + i['classroom']
        result += '\n' + '-----------------------'
        result = ''.join(result)

    return result


def all_schedule(sched, time=True, subgroup=False, lesson=True, teacher=False, classroom=False):
    sched = dict(json.loads(sched))

    result = ''
    for k, v in sched.items():
        if v == None:
            continue
        result += '\n' + str(WeekDays_RU[WeekDays_EN.index(k)]).title() + '\n'
        for i in v['lessons']:
            result += '\n' + '-------------------'
            if time:
                result += '\n' + 'Время: ' + i['time']['start'] + ':' + i['time']['end']
            if subgroup:
                result += '\n' + 'Подгруппа: ' + i['subgroup']
            if lesson:
                result += '\n' + 'Предмет: ' + i['lesson']
            if teacher:
                result += '\n' + 'Преподаватель: ' + i['teacher']
            if classroom:
                result += '\n' + 'Аудитория: ' + i['classroom']
            result += '\n' + '-------------------' + '\n'
            result = ''.join(result)

    return result


def current_lesson(sched, time=True, subgroup=True, lesson=True, teacher=True, classroom=True):
    now = dt.datetime.now()
    weekday = now.isoweekday() - 1
    day = WeekDays_EN[weekday]
    result, delta = None, None
    sched = dict(json.loads(sched))
    todays_sched = sched[day]
    current_time = now.strptime(now.strftime('%H:%M'), '%H:%M')
    amount_lessons = len(todays_sched)
    counter_lessons = 0
    end = 0

    for i in todays_sched['lessons']:
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

        result += '\n' + 'Время: ' + i['time']['start'] + ':' + i['time']['end']
        if subgroup:
            result += '\n' + 'Подгруппа: ' + i['subgroup']
        result += '\n' + 'Предмет: ' + i['lesson']
        if teacher:
            result += '\n' + 'Преподаватель: ' + i['teacher']
        if classroom:
            result += '\n' + 'Аудитория: ' + i['classroom']
        result = ''.join(result)

    return result

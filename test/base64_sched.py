import base64, re
from datetime import datetime, time

from schedule_json.change.change_sched import check_input
from vars import first_lesson, WeekDays_RU, WeekDays_EN

from vars import Sched

def sched_base64():
    sched = b'eydtb25kYXknOiBOb25lLCAndHVlc2RheSc6IHsnbGVzc29ucyc6IFt7J3RpbWUnOiB7J3N0YXJ0JzogJzEwOjQwJywgJ2VuZCc6ICcxMToyMCd9LCAnc3ViZ3JvdXAnOiAnJywgJ2xlc3Nvbic6ICfQodCY0KHQodCY0JEg0L/RgNCw0LouJywgJ3RlYWNoZXInOiAn0KHRg9C50LXRg9Cx0LDQtdCyINCeLiDQkS4g0YHRgi4g0L/RgNC10L8uJywgJ2NsYXNzcm9vbSc6ICfQntC90LvQsNC50L0nfSwgeyd0aW1lJzogeydzdGFydCc6ICcxMTo0MCcsICdlbmQnOiAnMTI6MjAnfSwgJ3N1Ymdyb3VwJzogJycsICdsZXNzb24nOiAn0KHQmNCh0KHQmNCRINC70LXQui4nLCAndGVhY2hlcic6ICfQodGD0LnQtdGD0LHQsNC10LIg0J4uINCRLiDRgdGCLiDQv9GA0LXQvy4nLCAnY2xhc3Nyb29tJzogJ9Ce0L3Qu9Cw0LnQvSd9XX0sICd3ZWRuZXNkYXknOiB7J2xlc3NvbnMnOiBbeyd0aW1lJzogeydzdGFydCc6ICcwOTo0MCcsICdlbmQnOiAnMTA6MjAnfSwgJ3N1Ymdyb3VwJzogJycsICdsZXNzb24nOiAn0KLQktCY0JzQoSDQv9GA0LDQui4nLCAndGVhY2hlcic6ICfQnNCw0YHQsNC90L7QstCwINCQLiDQli4g0LTQvtGGLicsICdjbGFzc3Jvb20nOiAn0J7QvdC70LDQudC9J30sIHsndGltZSc6IHsnc3RhcnQnOiAnMTA6NDAnLCAnZW5kJzogJzExOjIwJ30sICdzdWJncm91cCc6ICcnLCAnbGVzc29uJzogJ9Ci0JLQmNCc0KEg0L/RgNCw0LouJywgJ3RlYWNoZXInOiAn0JzQsNGB0LDQvdC+0LLQsCDQkC4g0JYuINC00L7Rhi4nLCAnY2xhc3Nyb29tJzogJ9Ce0L3Qu9Cw0LnQvSd9LCB7J3RpbWUnOiB7J3N0YXJ0JzogJzExOjQwJywgJ2VuZCc6ICcxMjoyMCd9LCAnc3ViZ3JvdXAnOiAnJywgJ2xlc3Nvbic6ICfQptChINC70LXQui4nLCAndGVhY2hlcic6ICfQkdC10YDQtNC40LHQsNC10LIg0KAuINCoLiDQtNC+0YYuJywgJ2NsYXNzcm9vbSc6ICfQntC90LvQsNC50L0nfSwgeyd0aW1lJzogeydzdGFydCc6ICcxMjo0MCcsICdlbmQnOiAnMTM6MjAnfSwgJ3N1Ymdyb3VwJzogJycsICdsZXNzb24nOiAn0KTQmiDQv9GA0LDQui4nLCAndGVhY2hlcic6ICfQk9C+0LvQvtCy0LDRhyDQnS4g0JguINGB0YIuINC/0YDQtdC/LicsICdjbGFzc3Jvb20nOiAn0J7QvdC70LDQudC9J31dfSwgJ3RodXJzZGF5JzogeydsZXNzb25zJzogW3sndGltZSc6IHsnc3RhcnQnOiAnMDk6NDAnLCAnZW5kJzogJzEwOjIwJ30sICdzdWJncm91cCc6ICcxJywgJ2xlc3Nvbic6ICfQptChINC70LDQsS4nLCAndGVhY2hlcic6ICfQlNC80LjRgtGA0LjQtdCy0LAg0JwuINCSLiDRgdGCLiDQv9GA0LXQvy4nLCAnY2xhc3Nyb29tJzogJ9Ce0L3Qu9Cw0LnQvSd9LCB7J3RpbWUnOiB7J3N0YXJ0JzogJzEwOjQwJywgJ2VuZCc6ICcxMToyMCd9LCAnc3ViZ3JvdXAnOiAnMScsICdsZXNzb24nOiAn0KbQoSDQu9Cw0LEuJywgJ3RlYWNoZXInOiAn0JTQvNC40YLRgNC40LXQstCwINCcLiDQki4g0YHRgi4g0L/RgNC10L8uJywgJ2NsYXNzcm9vbSc6ICfQntC90LvQsNC50L0nfSwgeyd0aW1lJzogeydzdGFydCc6ICcxMTo0MCcsICdlbmQnOiAnMTI6MjAnfSwgJ3N1Ymdyb3VwJzogJycsICdsZXNzb24nOiAn0KLQl9Ca0Jgg0LvQtdC6LicsICd0ZWFjaGVyJzogJ9CU0LzQuNGC0YDQuNC10LLQsCDQnC4g0JIuINGB0YIuINC/0YDQtdC/LicsICdjbGFzc3Jvb20nOiAn0J7QvdC70LDQudC9J30sIHsndGltZSc6IHsnc3RhcnQnOiAnMTQ6NDAnLCAnZW5kJzogJzE1OjIwJ30sICdzdWJncm91cCc6ICcnLCAnbGVzc29uJzogJ9CR0J7QoSDQu9C10LouJywgJ3RlYWNoZXInOiAn0KHQsNGC0LjQvNC+0LLQsCDQlS4g0JMuINC00L7Rhi4nLCAnY2xhc3Nyb29tJzogJ9Ce0L3Qu9Cw0LnQvSd9XX0sICdmcmlkYXknOiB7J2xlc3NvbnMnOiBbeyd0aW1lJzogeydzdGFydCc6ICcwOTo0MCcsICdlbmQnOiAnMTA6MjAnfSwgJ3N1Ymdyb3VwJzogJzEnLCAnbGVzc29uJzogJ9Ci0JfQmtCYINC70LDQsS4nLCAndGVhY2hlcic6ICfQlNC80LjRgtGA0LjQtdCy0LAg0JwuINCSLiDRgdGCLiDQv9GA0LXQvy4nLCAnY2xhc3Nyb29tJzogJ9Ce0L3Qu9Cw0LnQvSd9LCB7J3RpbWUnOiB7J3N0YXJ0JzogJzEwOjQwJywgJ2VuZCc6ICcxMToyMCd9LCAnc3ViZ3JvdXAnOiAnMScsICdsZXNzb24nOiAn0KLQl9Ca0Jgg0LvQsNCxLicsICd0ZWFjaGVyJzogJ9CU0LzQuNGC0YDQuNC10LLQsCDQnC4g0JIuINGB0YIuINC/0YDQtdC/LicsICdjbGFzc3Jvb20nOiAn0J7QvdC70LDQudC9J30sIHsndGltZSc6IHsnc3RhcnQnOiAnMTE6NDAnLCAnZW5kJzogJzEyOjIwJ30sICdzdWJncm91cCc6ICcnLCAnbGVzc29uJzogJ9Ci0JLQmNCc0KEg0LvQtdC6LicsICd0ZWFjaGVyJzogJ9Cc0LDRgdCw0L3QvtCy0LAg0JAuINCWLiDQtNC+0YYuJywgJ2NsYXNzcm9vbSc6ICfQntC90LvQsNC50L0nfV19LCAnc2F0dXJkYXknOiB7J2xlc3NvbnMnOiBbeyd0aW1lJzogeydzdGFydCc6ICcwOTo0MCcsICdlbmQnOiAnMTA6MjAnfSwgJ3N1Ymdyb3VwJzogJzEnLCAnbGVzc29uJzogJ9CR0J7QoSDQu9Cw0LEuJywgJ3RlYWNoZXInOiAn0JfQuNC80LjQvSDQmC4nLCAnY2xhc3Nyb29tJzogJ9Ce0L3Qu9Cw0LnQvSd9LCB7J3RpbWUnOiB7J3N0YXJ0JzogJzEwOjQwJywgJ2VuZCc6ICcxMToyMCd9LCAnc3ViZ3JvdXAnOiAnMScsICdsZXNzb24nOiAn0JHQntChINC70LDQsS4nLCAndGVhY2hlcic6ICfQl9C40LzQuNC9INCYLicsICdjbGFzc3Jvb20nOiAn0J7QvdC70LDQudC9J31dfX0='
    sched = sched.decode('utf-8')
    sched = base64.b64decode(sched.encode('utf-8')).decode("utf-8")
    sched = eval(sched)
    sched = Sched.parse_raw(sched)

def time_f():
    complex_time = '08:40 - 09:20'
    complex_time = re.findall(r'(\d{1,2}[.:]\d{2})[- ]*(\d{1,2}[.:]\d{2})', complex_time)
    return list(complex_time[0])

def get_lessons_time(day_of_week: str, sched: dict):
    day_of_week = WeekDays_RU.index(day_of_week)
    if check_input(day_of_week) == -1:
        return -1
    day = WeekDays_EN[day_of_week]
    sched: dict = Sched.parse_obj(sched).dict()
    start, end, lesson_time, lessons = [], [], [], []
    if sched[day] is None:
        return []
    else:
        for i in range(len(sched[day]['lessons'])):
            lessons.append(sched[day]['lessons'][i])
            start.append(datetime.strptime(str(sched[day]['lessons'][i]['time']['start']), "%H:%M").time())
            end.append(datetime.strptime(str(sched[day]['lessons'][i]['time']['end']), "%H:%M").time())
        for t in range(13):
            t_start = time(hour=first_lesson.hour + 1 * t, minute=first_lesson.minute)
            t_end = time(hour=first_lesson.hour + 1 * (t + 1), minute=first_lesson.minute - 20)
            if t_start in start:
                lesson_time.append(str(lessons[(start.index(t_start))]['lesson']))
                #lesson_time.append(t_start.strftime("%H:%M") + ' - ' + t_end.strftime("%H:%M"))
    print('lesson_time: ' + str(lesson_time))
    return lesson_time

get_lessons_time('вторник', eval("{'monday': {'lessons': [{'time': {'start': '08:40', 'end': '09:20'}, 'subgroup': 'None', 'lesson': 'qwe', 'teacher': 'qwe', 'classroom': 'qwe'}]}, 'tuesday': {'lessons': [{'time': {'start': '10:40', 'end': '11:20'}, 'subgroup': '', 'lesson': 'СИССИБ прак.', 'teacher': 'Суйеубаев О. Б. ст. преп.', 'classroom': 'Онлайн'}, {'time': {'start': '11:40', 'end': '12:20'}, 'subgroup': '', 'lesson': 'СИССИБ лек.', 'teacher': 'Суйеубаев О. Б. ст. преп.', 'classroom': 'Онлайн'}]}, 'wednesday': {'lessons': [{'time': {'start': '09:40', 'end': '10:20'}, 'subgroup': '', 'lesson': 'ТВИМС прак.', 'teacher': 'Масанова А. Ж. доц.', 'classroom': 'Онлайн'}, {'time': {'start': '10:40', 'end': '11:20'}, 'subgroup': '', 'lesson': 'ТВИМС прак.', 'teacher': 'Масанова А. Ж. доц.', 'classroom': 'Онлайн'}, {'time': {'start': '11:40', 'end': '12:20'}, 'subgroup': '', 'lesson': 'ЦС лек.', 'teacher': 'Бердибаев Р. Ш. доц.', 'classroom': 'Онлайн'}, {'time': {'start': '12:40', 'end': '13:20'}, 'subgroup': '', 'lesson': 'ФК прак.', 'teacher': 'Головач Н. И. ст. преп.', 'classroom': 'Онлайн'}]}, 'thursday': {'lessons': [{'time': {'start': '09:40', 'end': '10:20'}, 'subgroup': '1', 'lesson': 'ЦС лаб.', 'teacher': 'Дмитриева М. В. ст. преп.', 'classroom': 'Онлайн'}, {'time': {'start': '10:40', 'end': '11:20'}, 'subgroup': '1', 'lesson': 'ЦС лаб.', 'teacher': 'Дмитриева М. В. ст. преп.', 'classroom': 'Онлайн'}, {'time': {'start': '11:40', 'end': '12:20'}, 'subgroup': '', 'lesson': 'ТЗКИ лек.', 'teacher': 'Дмитриева М. В. ст. преп.', 'classroom': 'Онлайн'}, {'time': {'start': '14:40', 'end': '15:20'}, 'subgroup': '', 'lesson': 'БОС лек.', 'teacher': 'Сатимова Е. Г. доц.', 'classroom': 'Онлайн'}]}, 'friday': {'lessons': [{'time': {'start': '09:40', 'end': '10:20'}, 'subgroup': '1', 'lesson': 'ТЗКИ лаб.', 'teacher': 'Дмитриева М. В. ст. преп.', 'classroom': 'Онлайн'}, {'time': {'start': '10:40', 'end': '11:20'}, 'subgroup': '1', 'lesson': 'ТЗКИ лаб.', 'teacher': 'Дмитриева М. В. ст. преп.', 'classroom': 'Онлайн'}, {'time': {'start': '11:40', 'end': '12:20'}, 'subgroup': '', 'lesson': 'ТВИМС лек.', 'teacher': 'Масанова А. Ж. доц.', 'classroom': 'Онлайн'}]}, 'saturday': {'lessons': [{'time': {'start': '09:40', 'end': '10:20'}, 'subgroup': '1', 'lesson': 'БОС лаб.', 'teacher': 'Зимин И.', 'classroom': 'Онлайн'}, {'time': {'start': '10:40', 'end': '11:20'}, 'subgroup': '1', 'lesson': 'БОС лаб.', 'teacher': 'Зимин И.', 'classroom': 'Онлайн'}]}}"))


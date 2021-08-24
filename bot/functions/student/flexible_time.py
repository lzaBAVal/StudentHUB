import re
from datetime import datetime


def check_flex_time(time_lesson):
    print(f'time_lesson: {time_lesson}')
    if not re.match(r'\d{1,2}[: /]\d{1,2}.{1,3}\d{1,2}[: /]\d{1,2}', time_lesson):
        return False
    a = re.search(r'(\d{1,2})[: /](\d{1,2})[ ]{0,1}.[ ]{0,1}(\d{1,2})[: /](\d{1,2})', time_lesson).groups()
    print(f'a: {a}')
    a = [int(i) for i in list(a)]
    if 23 > a[2] > 7 and 23 > a[0] > 7 and a[1] % 5 == 0 and a[3] % 5 == 0:
        if a[0] < a[2] or (a[0] == a[2] and a[1] < a[3]):
            print(True)
            return True
    print(False)
    return False


def test_minus_time(start, end, time_lesson_start, time_lesson_end):
    samples_start = start
    samples_end = end

    result_lst, save_time_end, save_time_start = [], [], []

    def strToTime(lst):
        res = []
        for i in lst:
            res.append(datetime.strptime(i, "%H:%M"))
        return res

    if start == [] and end == []:
        for i in range(len(time_lesson_start)):
            result_lst.append(f'{time_lesson_start[i].time().strftime("%H:%M")} - '
                              f'{time_lesson_end[i].time().strftime("%H:%M")}')
        return result_lst

    for t in range(len(samples_start)):
        for i in range(len(time_lesson_start)):
            if time_lesson_start[i].hour == samples_start[t].hour:
                if i == 0:
                    a = i
                else:
                    a = i if samples_start[t].minute >= 40 else i - 1
                save_time_start.append(time_lesson_start[a])
            if time_lesson_end[i].hour == samples_end[t].hour:
                if i == len(time_lesson_start) - 1:
                    a = i
                else:
                    a = i if samples_end[t].minute <= 20 else i + 1
                save_time_end.append(time_lesson_end[a])
    # print(f'save_time_start: {[i.strftime("%X") for i in save_time_start]}')
    # print(f'save_time_end: {[i.strftime("%X") for i in save_time_end]}')
    # print(f'len(time_lesson_start): {len(time_lesson_start)}')
    # print(f'time_lesson_start: {time_lesson_start}')
    flag = 0
    for j in range(len(save_time_start)):
        for i in range(len(time_lesson_start)):
            if time_lesson_start[i] == save_time_start[j]:
                flag = 1
                time_lesson_start[i] = 0
            if time_lesson_end[i] == save_time_end[j]:
                flag = 0
                time_lesson_start[i] = 0
                time_lesson_end[i] = 0
            elif flag == 1:
                time_lesson_start[i] = 0
                time_lesson_end[i] = 0
            else:
                pass

    for i in range(len(time_lesson_start)):
        if time_lesson_start[i] != 0:
            # print(f'time_lesson_start[{i}]: {time_lesson_start[i]}')
            result_lst.append(f'{time_lesson_start[i].time().strftime("%H:%M")} - '
                              f'{time_lesson_end[i].time().strftime("%H:%M")}')

    return result_lst



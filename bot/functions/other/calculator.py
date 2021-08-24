'''
    calc_basic -> данной функции будут скармливаться текущий рейтинг и желаемая оценка.
    В случае если пользователь неверно введет оценки, выдастся ошибка и придет оповещение, говорящее о направильном
    вводе данных.
    Если студент явно укажет какую оценку он желает, произведется расчет только этой оценки, в ином случае вернется
    ответ с несколькими оценками.
'''
import math


def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def calc_basic(rating: float, target: float = 0):
    if (rating > 0) and (target >= 0) and (rating <= 100) and (target <= 100):
        if target == 0:
            target = [95, 90, 80, 75, 70, 50]
            result = []
            for i in target:
                interm_res = (i - 0.6 * rating) / 0.4
                result.append(int_r(interm_res))
            res = ''
            for i in range(len(target)):
                if i == 0:
                    res += f'Итог => Сколько необходимо получить на экзамене\n'
                if target[i] == 70 and 50 <= result[i] <= 100:
                    res += f'Для сохранения стипендии - '
                if target[i] == 70 and result[i] < 50:
                    res += f'Для сохранения стипендии (70) - ≥ 50'
                if 50 <= result[i] <= 100:
                    res += f'{target[i]} => {result[i]}\n'
            return res
        else:
            return (target - 0.6 * rating) / 0.4
    else:
        return -1


def calc_advanced():
    pass

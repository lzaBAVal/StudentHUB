'''
    calc_basic -> данной функции будут скармливаться текущий рейтинг и желаемая оценка.
    В случае если пользователь неверно введет оценки, выдастся ошибка и придет оповещение, говорящее о направильном
    вводе данных.
    Если студент явно укажет какую оценку он желает, произведется расчет только этой оценки, в ином случае вернется
    ответ с несколькими оценками.
'''


def calc_basic(rating: float, target: float = 0):
    if (rating > 0) and (target >= 0) and (rating <= 100) and (target <= 100):
        if target == 0:
            target = [100, 90, 80, 75, 70, 50]
            result = []
            for i in target:
                interm_res = (i - 0.6 * rating) / 0.4
                result.append(interm_res)
            return target, result
        else:
            return (target - 0.6 * rating) / 0.4
    else:
        return -1


def calc_advanced():
    pass


print(calc_basic(50, 100))

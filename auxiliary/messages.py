state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}", что удовлетворяет условию "один из {states}"'

calc_error = 'Произошла ошибка при расчете оценки. Пожалуйста проверьте еще раз оценки которые вы вводите. В случае ' \
             'если вы считаете, что вводите все верно, сообщите об этом случае админу.'
calc_one_result = 'Для желаемой итоговой оценки на экзамене вам необходимо '\
                  'получить "{0}"\nУдачи!'
calc_many_result = 'Для получения {0} баллов нужно получить {1}'
calc_many_result_reuse = 'Для {0} - {1}'

wtf_error = 'Что-то произошло, о проблеме пиши админу!'

def calc_output(rating) -> str:
    if rating == -1:
        return calc_error
    elif type(rating) == float:
        return calc_one_result.format(rating)
    elif type(rating) == tuple:
        target = rating[0]
        rating = rating[1]
        res = []
        for i in range(len(rating)):
            if i == 0:
                res.append((calc_many_result.format(target[i], rating[i])))
            else:
                res.append((calc_many_result_reuse.format(target[i], rating[i])))
        return "\n".join(res)
    else:
        return wtf_error

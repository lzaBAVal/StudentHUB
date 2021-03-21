from aiogram.types import ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from schedule_json.vars import WeekDays_EN, WeekDays_RU

all_shedule_btn = KeyboardButton("Все расписание")
next_lesson_btn = KeyboardButton("Cледующая пара")
todays_shedule_btn = KeyboardButton("Расписание на сегодня")

rating_btn = KeyboardButton("Расчитать итоговую оценку")
alert_btn = KeyboardButton("Настройка уведомлений")
find_group_btn = KeyboardButton("Найти группу")

register_btn = KeyboardButton("Регистрация")
register_cancel = KeyboardButton("Отменить регистрацию")
register_yes = KeyboardButton("Да")
register_no = KeyboardButton("Нет")

keys_btn = KeyboardButton("У меня есть ключ")

change_sched_btn = KeyboardButton("Изменить расписание")
add_lesson_btn = KeyboardButton("Добавить урок")
delete_lesson_btn = KeyboardButton("Убрать урок")
replace_lesson_btn = KeyboardButton("Заменить урок")

subgroup1_btn = KeyboardButton("1")
subgroup2_btn = KeyboardButton("2")
subgroup3_btn = KeyboardButton("3")

cat_btn = '🐈'

stud_kb = ReplyKeyboardMarkup(resize_keyboard=True)
stud_kb.row(all_shedule_btn, next_lesson_btn, todays_shedule_btn)
stud_kb.add(change_sched_btn)
stud_kb.row(alert_btn, rating_btn)

tester_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
tester_kb.add(keys_btn)

anon_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
anon_kb.row(register_btn)

question_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
question_kb.row(register_yes, register_no)

register_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
register_kb.add(register_cancel)

change_sched_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_sched_kb.row(add_lesson_btn, delete_lesson_btn, replace_lesson_btn)

subgroup_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
subgroup_kb.row(subgroup1_btn, subgroup2_btn, subgroup3_btn)

cat_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cat_kb.row(cat_btn)


def createButtons(btns_l: list):
    group = []
    for i in btns_l:
        group.append(i)
    test = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(group)):
        if i % 2 == 0:
            test.row(KeyboardButton(str(group[i])))
        else:
            test.add(KeyboardButton(str(group[i])))
        test.add(register_cancel)
    return test


def days():
    days_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(WeekDays_RU)):
        days_kb.add(WeekDays_RU[i])
        if i == 3:
            days_kb.row()

    return days_kb

def free_time(time: list):
    free_time_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in time:
        free_time_kb.add(i)
    return free_time_kb

# greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)

# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
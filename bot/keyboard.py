from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton
from vars import WeekDays_RU

all_shedule_btn = KeyboardButton("Все расписание")
next_lesson_btn = KeyboardButton("Cледующая пара")
todays_shedule_btn = KeyboardButton("Расписание на сегодня")
tommorow_shedule_btn = KeyboardButton("Расписание на завтра")
back_to_menu_btn = KeyboardButton("Вернуться на главное меню")

rating_btn = KeyboardButton("Расчитать итоговую оценку")
alert_btn = KeyboardButton("Настройка уведомлений")
find_group_btn = KeyboardButton("Найти группу")

register_btn = KeyboardButton("Регистрация")
cancel_btn = KeyboardButton("Отменить регистрацию")
yes_btn = KeyboardButton("Да")
no_btn = KeyboardButton("Нет")

keys_btn = KeyboardButton("У меня есть ключ")

change_sched_btn = KeyboardButton("Изменить расписание")
add_lesson_btn = KeyboardButton("Добавить урок")
delete_lesson_btn = KeyboardButton("Убрать урок")
replace_lesson_btn = KeyboardButton("Заменить урок")

subgroup_no_btn = KeyboardButton("Нет подгрупп")
subgroup1_btn = KeyboardButton("1")
subgroup2_btn = KeyboardButton("2")
subgroup3_btn = KeyboardButton("3")

classroom_online_btn = KeyboardButton("Онлайн")

cat_btn = '🐈'

stud_kb = ReplyKeyboardMarkup(resize_keyboard=True)
stud_kb.row(next_lesson_btn, todays_shedule_btn,tommorow_shedule_btn, all_shedule_btn)
stud_kb.add(change_sched_btn)
#stud_kb.row(alert_btn, rating_btn)

tester_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
tester_kb.add(keys_btn)

anon_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
anon_kb.row(register_btn)

question_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
question_kb.row(yes_btn, no_btn)

register_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
register_kb.add(cancel_btn)

change_sched_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_sched_kb.row(add_lesson_btn, delete_lesson_btn)
change_sched_kb.add(back_to_menu_btn)

subgroup_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
subgroup_kb.row(subgroup_no_btn, subgroup1_btn, subgroup2_btn, subgroup3_btn)
subgroup_kb.add(cancel_btn)

classroom_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
classroom_kb.add(classroom_online_btn, cancel_btn)

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
    test.add(cancel_btn)
    return test


def days():
    days_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(WeekDays_RU) - 1):
        days_kb.add(WeekDays_RU[i].capitalize())
        if i == 3:
            days_kb.row()
    days_kb.add(cancel_btn)
    return days_kb


def free_time(time: list):
    free_time_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(len(time)):
        if i % 3 == 0:
            free_time_kb.row(time[i])
        else:
            free_time_kb.add(time[i])
    free_time_kb.add(cancel_btn)
    return free_time_kb

# greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)

# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.strings.commands import *
from vars import WeekDays_RU

all_shedule_btn = KeyboardButton(all_schedule_str)
next_lesson_btn = KeyboardButton(next_lesson_str)
todays_shedule_btn = KeyboardButton(todays_shedule_str)
tommorow_shedule_btn = KeyboardButton(tommorow_shedule_str)
configuration_btn = KeyboardButton(configuration_str)
back_to_menu_btn = KeyboardButton(back_to_menu_str)

rating_btn = KeyboardButton(rating_str)
alert_btn = KeyboardButton(alert_str)
find_group_btn = KeyboardButton(find_group_str)

register_btn = KeyboardButton(register_str)
cancel_btn = KeyboardButton(cancel_str)
yes_btn = KeyboardButton(yes_str)
no_btn = KeyboardButton(no_str)

keys_btn = KeyboardButton(keys_str)

change_sched_btn = KeyboardButton(change_sched_str)
add_lesson_btn = KeyboardButton(add_lesson_str)
delete_lesson_btn = KeyboardButton(delete_lesson_str)
replace_lesson_btn = KeyboardButton(register_str)

personal_schedule_btn = KeyboardButton(personal_schedule_str)
group_schedule_btn = KeyboardButton(group_schedule_str)

whose_schedule_btn = KeyboardButton(whose_schedule_str)

subgroup_no_btn = KeyboardButton("Нет подгрупп")
subgroup1_btn = KeyboardButton("1")
subgroup2_btn = KeyboardButton("2")
subgroup3_btn = KeyboardButton("3")

classroom_online_btn = KeyboardButton("Онлайн")

cat_btn = '🐈'

stud_kb = ReplyKeyboardMarkup(resize_keyboard=True)
stud_kb.add(next_lesson_btn, todays_shedule_btn)
stud_kb.add(tommorow_shedule_btn, all_shedule_btn)
stud_kb.add(change_sched_btn)
stud_kb.add(configuration_btn)

tester_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
tester_kb.add(keys_btn)

anon_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
anon_kb.row(register_btn)

question_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
question_kb.row(yes_btn, no_btn)
question_kb.add(cancel_btn)

register_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
register_kb.add(cancel_btn)

change_sched_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_sched_kb.row(add_lesson_btn, delete_lesson_btn)
change_sched_kb.add(back_to_menu_btn)

which_sched_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
which_sched_kb.row(personal_schedule_btn, group_schedule_btn)

subgroup_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
subgroup_kb.row(subgroup_no_btn, subgroup1_btn, subgroup2_btn, subgroup3_btn)
subgroup_kb.add(cancel_btn)

classroom_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
classroom_kb.add(classroom_online_btn, cancel_btn)

cat_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cat_kb.row(cat_btn)

configuration_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
configuration_kb.add(whose_schedule_btn)
configuration_kb.add(back_to_menu_btn)

select_whose_schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
select_whose_schedule_kb.row(personal_schedule_btn, group_schedule_btn)
select_whose_schedule_kb.add(back_to_menu_btn)


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

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.strings.commands import *
from schedule_json.output.get_schedule_object import parse_sched_parts, compose_sched_parts
from vars import WeekDays_RU

schedule_output_btn = KeyboardButton(schedule_output_str)
all_shedule_btn = KeyboardButton(all_schedule_str)
next_lesson_btn = KeyboardButton(next_lesson_str)
todays_shedule_btn = KeyboardButton(todays_shedule_str)
tommorow_shedule_btn = KeyboardButton(tommorow_shedule_str)
configuration_btn = KeyboardButton(configuration_str)
back_to_menu_btn = KeyboardButton(back_to_menu_str)
academic_task_btn = KeyboardButton(academic_task_str)
manage_group_btn = KeyboardButton(manage_group_str)
other_btn = KeyboardButton(other_str)
subject_add_btn = KeyboardButton(subject_add_str)
subject_delete_btn = KeyboardButton(subject_delete_str)
configure_subject_btn = KeyboardButton(configure_subject_str)

calculator_btn = KeyboardButton(calculator_str)
calendar_plan_btn = KeyboardButton(calendar_plan_str)

notifications_btn = KeyboardButton(notifications_str)
configure_schedule_btn = KeyboardButton(configure_schedule_str)
switch_language_btn = KeyboardButton(switch_language_str)
about_authors_btn = KeyboardButton(about_authors_str)

rating_btn = KeyboardButton(rating_str)
alert_btn = KeyboardButton(alert_str)
find_group_btn = KeyboardButton(find_group_str)

skip_finish_btn = KeyboardButton(skip_finish_str)
skip_btn = KeyboardButton(skip_str)
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

add_task_btn = KeyboardButton(add_task_str)
delete_task_btn = KeyboardButton(delete_task_str)
show_tasks_btn = KeyboardButton(show_tasks_str)
subjects_btn = KeyboardButton(subjects_str)
show_task_info_btn = KeyboardButton(show_task_info_str)
take_variant_btn = KeyboardButton(take_variant_str)

finish_configuration_btn = KeyboardButton(finish_configuration_str)

subgroup_no_btn = KeyboardButton("Нет подгрупп")
subgroup1_btn = KeyboardButton("1")
subgroup2_btn = KeyboardButton("2")
subgroup3_btn = KeyboardButton("3")

classroom_online_btn = KeyboardButton("Онлайн")

cat_btn = '🐈'

'''
stud_kb = ReplyKeyboardMarkup(resize_keyboard=True)
stud_kb.add(next_lesson_btn, todays_shedule_btn)
stud_kb.add(tommorow_shedule_btn, all_shedule_btn)
stud_kb.add(change_sched_btn)
stud_kb.add(configuration_btn)
'''


# Students keyboard
def stud_kb(privilege='u'):
    _stud_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if privilege == 'c':
        _stud_kb.add(next_lesson_btn, schedule_output_btn)
        _stud_kb.add(academic_task_btn)
        _stud_kb.add(manage_group_btn)
        _stud_kb.add(other_btn)
    else:
        _stud_kb.add(next_lesson_btn, schedule_output_btn)
        _stud_kb.add(academic_task_btn)
        _stud_kb.add(other_btn)
    return _stud_kb


# Cancel keyboard
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kb.add(cancel_btn)

# Skip keyboard
skip_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
skip_kb.add(skip_btn)
skip_kb.add(cancel_btn)

# Skip&finish work
skip_finish_kb = ReplyKeyboardMarkup(resize_keyboard=True)
skip_finish_kb.add(skip_finish_btn)
skip_finish_kb.add(cancel_btn)

# Other menu
other_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
other_kb.row(calculator_btn, calendar_plan_btn)
other_kb.add(configure_subject_btn)
other_kb.add(configuration_btn)
other_kb.add(back_to_menu_btn)

# Configure objects
subject_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
subject_kb.row(subject_add_btn, subject_delete_btn)
subject_kb.add(back_to_menu_btn)

# General configuration
configuration_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
configuration_kb.add(configure_schedule_btn)
configuration_kb.add(notifications_btn, switch_language_btn)
configuration_kb.add(about_authors_btn)
configuration_kb.add(back_to_menu_btn)

# Configure schedule
configure_schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
configure_schedule_kb.add(whose_schedule_btn)
configure_schedule_kb.add(back_to_menu_btn)

# Testers keyboard
tester_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
tester_kb.add(keys_btn)

# Anons keyboard
anon_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
anon_kb.row(register_btn)

# Question yes or no + cancel function
question_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
question_kb.row(yes_btn, no_btn)
question_kb.add(cancel_btn)

# Keyboard for registration
register_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
register_kb.add(cancel_btn)

# Change schedule
change_sched_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_sched_kb.row(add_lesson_btn, delete_lesson_btn)
change_sched_kb.add(back_to_menu_btn)

# Configure which keyboard we will use
which_sched_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
which_sched_kb.row(personal_schedule_btn, group_schedule_btn)

# Select group when add new lesson
subgroup_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
subgroup_kb.row(subgroup_no_btn, subgroup1_btn, subgroup2_btn, subgroup3_btn)
subgroup_kb.add(cancel_btn)

# Select classroom when add new lesson
classroom_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
classroom_kb.add(classroom_online_btn, cancel_btn)

# Tap on cat
cat_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cat_kb.row(cat_btn)

# Configure which keyboard we will use
select_whose_schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
select_whose_schedule_kb.row(personal_schedule_btn, group_schedule_btn)
select_whose_schedule_kb.add(back_to_menu_btn)

# Manage tasks
manage_task_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
manage_task_kb.row(add_task_btn, delete_task_btn)
manage_task_kb.add(subjects_btn)
manage_task_kb.add(show_tasks_btn)
manage_task_kb.add(back_to_menu_btn)

# Task menu
task_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
task_menu_kb.row(show_task_info_btn, take_variant_btn)
task_menu_kb.add(cancel_btn)


def createButtons(btns_l: list):
    group = []
    for i in btns_l:
        group.append(i)
    test = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in group:
        test.add(KeyboardButton(str(i)))
    test.add(cancel_btn)
    return test


def createX3Buttons(btns_l: list):
    row = []
    flag = False
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(btns_l)):
        if i % 3 == 0:
            kb.row(row)
            row = [KeyboardButton(str(btns_l[i]))]
            flag = False
        else:
            row.append(KeyboardButton(str(btns_l[i])))
            flag = True
    if flag:
        kb.row(row)
    kb.add(cancel_btn)
    return kb


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
        if i % 2 != 0:
            free_time_kb.row(time[i])
        else:
            free_time_kb.add(time[i])
    free_time_kb.add(cancel_btn)
    return free_time_kb


def sched_parts_kb(parts: str) -> dict:
    parts_text = {
        'lesson': 'Название предмета ',
        'time': 'Время занятия ',
        'subgroup': 'Подгруппа ',
        'teacher': 'Имя преподавателя ',
        'classroom': 'Кабинет '
    }
    buttons = []
    parts = parse_sched_parts(parts)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    text = parts_text
    kb.add(finish_configuration_btn)
    for part in parts_text:
        if bool(parts[part]):
            text[part] += '✔️'
        else:
            text[part] += '❌'
        buttons.append(createOneButton(parts_text[part]))
    for i in range(0, len(buttons), 2):
        if len(buttons) - i >= 2:
            kb.row(buttons[i], buttons[i + 1])
        else:
            kb.row(buttons[i])
    return kb


def update_sched_parts(parts: str, msg: str) -> [str, None]:
    parts = parse_sched_parts(parts)
    text: dict = {
        'lesson': ['Название предмета ✔️', 'Название предмета ❌'],
        'time': ['Время занятия ✔️', 'Время занятия ❌'],
        'subgroup': ['Подгруппа ✔️', 'Подгруппа ❌'],
        'teacher': ['Имя преподавателя ✔️', 'Имя преподавателя ❌'],
        'classroom': ['Кабинет ✔️', 'Кабинет ❌']
    }
    count = 0
    for i in text:
        if msg in text[i]:
            if count == 0:
                parts[i] = not parts[i]
            else:
                parts[i] = not parts[i]
            return compose_sched_parts(parts)
        count += 1
    return None


def createOneButton(text):
    button = KeyboardButton(text)
    return button


def show_tasks_kb(subjects: dict):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    subjects_dict = {}
    for subject in subjects:
        for task in subjects[subject]:
            for name in task:
                result_str = f'{subject}: {name}'
                markup.add(result_str)
                subjects_dict.setdefault(result_str, task[name])
    markup.add(cancel_btn)
    return markup, subjects_dict


def show_subjects_kb(subjects: dict):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    subjects_dict = {}
    for subject in subjects:
        for task in subjects[subject]:
            for name in task:
                result_str = f'{subject}: {name}'
                markup.add(result_str)
                subjects_dict.setdefault(result_str, task[name])
    markup.add(cancel_btn)
    return markup, subjects_dict

##################
# InlineKeyboard #
##################


delete_cb = CallbackData('delete', 'action')


def get_delete_message_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '❌',
            callback_data=delete_cb.new(action='delete'))
    )
    return markup

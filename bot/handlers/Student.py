import datetime
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from bot.keyboard.keyboard import configuration_kb, change_sched_kb, days, stud_kb, question_kb, other_kb, \
    configure_schedule_kb, cancel_kb, skip_finish_kb, skip_btn, skip_kb, manage_task_kb
from bot.states.states import StudentStates, AddLesson, DeleteLesson, DiscoverFreeTime, SetCaptainState, \
    Calculate, CreateNewTask
from bot.strings.messages import *
from bot.strings.commands import *
from functions.command import delete_user
from functions.other.calculator import calc_basic
from functions.other.parse_variants import parse_variant
from functions.student.add_photo import keep_photo, save_photo
from functions.student.change_schedule import check_privilege_whose

from functions.student.get_schedule import get_all_schedule, get_todays_shedule, get_next_lesson, get_tommorow_lesson, \
    get_output_free_time
from loader import db
from misc import dp
from models import Group, Student, Photo, Subject
from models.task import Task
from task_subject.harvest import add_object_for_group
from old_config import PATH_WIN

from utils.log.logging_core import init_logger

from functions.student.other import get_list_of_classmates, get_bio

logger = init_logger()
app_dir: Path = Path(__file__)


# BACK TO MENU
@dp.message_handler(Text(equals=back_to_menu_str, ignore_case=True), state=StudentStates.student)
async def back_to_menu(message: types.Message, state: FSMContext):
    privilege = (await state.get_data())['captain_middleware']
    await message.answer('Вы в главном меню', reply_markup=stud_kb(privilege))


# MENU OTHER
@dp.message_handler(Text(equals=other_str, ignore_case=True), state=StudentStates.student)
async def menu_other(message: types.Message):
    await message.answer(text=f'Панель "{other_str}"', reply_markup=other_kb)


# MENU CONFIGURE SCHEDULE
@dp.message_handler(Text(equals=configure_schedule_str, ignore_case=True), state=StudentStates.student)
async def menu_configure_schedule(message: types.Message):
    await message.answer(text=f'Панель "{configure_schedule_str}"', reply_markup=configure_schedule_kb)


# MENU MANAGE TASKS
@dp.message_handler(Text(equals=academic_task_str, ignore_case=True), state=StudentStates.student)
async def menu_academic_task(message: types.Message):
    await message.answer(text=f'Меню "{academic_task_str}"', reply_markup=manage_task_kb)


# GET PHOTO
@dp.message_handler(Text(equals='cat', ignore_case=True), state=StudentStates.student)
async def get_photo(message: types.Message):
    hash = await Photo.all().first().values_list('file_id')
    hash = str(hash[0][0])
    await message.answer_photo(InputFile(Path(f"{PATH_WIN}\{hash[:2]}\{hash[:4]}\{hash}.jpg")))
    # await message.answer_photo(InputFile(Path('FS/tmp/tmp_files.jpg')))


# GET ALL SCHEDULE
@dp.message_handler(Text(equals=all_schedule_str, ignore_case=True), state=StudentStates.student)
async def all_shedule_student(message: types.Message):
    await get_all_schedule(message)


# GET TODAYS LESSONS
@dp.message_handler(Text(equals=todays_shedule_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def todays_shedule(message: types.Message):
    await get_todays_shedule(message)


# GET NEXT LESSON
@dp.message_handler(Text(equals=next_lesson_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def next_lesson(message: types.Message):
    await get_next_lesson(message)


# GET TOMMOROW LESSON
@dp.message_handler(Text(equals=tommorow_shedule_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def tommorow_lesson(message: types.Message):
    await get_tommorow_lesson(message)


# CHANGE CONFIGURATION
@dp.message_handler(Text(equals=configuration_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите изменить в настройках?', reply_markup=configuration_kb)


# CHANGE SCHEDULE
@dp.message_handler(Text(equals=change_sched_str,
                         ignore_case=True),
                    state=StudentStates.student,
                    is_captain=True)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=change_sched_kb)


# ADD LESSON INITIAL
@dp.message_handler(Text(equals=add_lesson_str,
                         ignore_case=True),
                    state=StudentStates.student, is_captain=True)
async def add_lesson_start(message: types.message):
    if (await check_privilege_whose(message, privilege=True)) == 0:
        await message.answer('В какой день вы хотите добавить урок?', reply_markup=days())
        await AddLesson.time.set()


# DELETE LESSON INITIAL
@dp.message_handler(Text(equals=delete_lesson_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def add_lesson_process_yes(message: types.message):
    if (await check_privilege_whose(message, privilege=True)) == 0:
        await message.answer('Выберите день:', reply_markup=days())
        await DeleteLesson.lesson.set()


# GET FREE TIME OF DAY 1
@dp.message_handler(Text(equals=discover_free_time_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def discover_free_time(message: types.message):
    await message.answer('Выберите день:', reply_markup=days())
    await DiscoverFreeTime.output.set()


# GET FREE TIME OF DAY 2
@dp.message_handler(state=DiscoverFreeTime.output)
async def output_free_time(message: types.message):
    await get_output_free_time(message)


# CALCULATE THE SCORE
@dp.message_handler(Text(equals=calculator_str,
                         ignore_case=True),
                    state=StudentStates.student)
async def calculate_score(message: types.message):
    await message.answer('Напишите ваш рейтинг допуска')
    await Calculate.score.set()


# INPUT SCORE
@dp.message_handler(state=Calculate.score)
async def calculate_score(message: types.message):
    if isinstance(int(message.text), int):
        score = calc_basic(int(message.text))
        await message.answer(score, reply_markup=stud_kb())
    else:
        await message.answer('Неверный ввод!', reply_markup=stud_kb())
    await StudentStates.student.set()


# GET INFO ABOUT STUDENT
@dp.message_handler(commands=['bio'], state=StudentStates.student)
async def bio(message: types.Message):
    result = await get_bio(message.chat.id)
    await message.answer(result)


# DELETE USER ACCOUNT
@dp.message_handler(commands=['deleteme'], state=StudentStates.student)
async def deleteme(message: types.Message):
    await delete_user(message)


# GET HELP FOR STUDENT
@dp.message_handler(commands=['help'], state=StudentStates.student)
async def check_user(message: types.Message):
    await message.answer(help_user_text)


# GET CURRENT TIME
@dp.message_handler(commands=['time'], state=StudentStates.student)
async def next_lesson(message: types.Message):
    await message.answer(str(datetime.datetime.now()))


# GET CLASSMATES
@dp.message_handler(commands=['classmates'], state=StudentStates.student)
async def classmates(message: types.Message):
    await message.answer(await get_list_of_classmates(db, message.chat.id))


# CAPTAIN ZONE
@dp.message_handler(commands=['help_captain'], state=StudentStates.student)
async def help_captain_privilege(message: types.Message):
    await message.answer(help_captain_str)


# TAKE PRIVILEGE
@dp.message_handler(commands=['captain_privilege'], state=StudentStates.student)
async def captain_privilege(message: types.Message):
    await message.answer('Введите пожалуйста ключ')
    await SetCaptainState.set.set()


# LOCK GROUP
@dp.message_handler(commands=['lock_group'], state=StudentStates.student)
async def captain_privilege(message: types.Message, state: FSMContext):
    if (await state.get_data([]))['captain_middleware'] is True:
        group_id = await Student.all().filter(id_chat=message.chat.id).first().values_list('group_id')
        group_id = group_id[0][0]
        await Group.filter(id_inc=group_id).update(lock=True)
        await message.answer('Вы закрыли вход в свою группу')


# UNLOCK GROUP
@dp.message_handler(commands=['unlock_group'], state=StudentStates.student)
async def captain_privilege(message: types.Message, state: FSMContext):
    if (await state.get_data())['captain_middleware'] is True:
        group_id = await Student.all().filter(id_chat=message.chat.id).first().values_list('group_id')
        group_id = group_id[0][0]
        await Group.filter(id_inc=group_id).update(lock=False)
        await message.answer('Вы открыли вход в свою группу всем. ')


# NO COMMAND
@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text='Я не понимаю что вы хотите', reply_markup=stud_kb())

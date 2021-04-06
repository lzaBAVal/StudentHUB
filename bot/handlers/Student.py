import datetime

from aiogram import types

from bot import keyboard as kb
from bot.states.states import StudentStates, AddLesson, DeleteLesson, DiscoverFreeTime
from bot.strings.messages import *
from bot.strings.commands import *
from functions.command import delete_user

from functions.student.get_schedule import get_all_schedule, get_todays_shedule, get_next_lesson, get_tommorow_lesson, \
    get_output_free_time
from loader import dp, db
from logs.logging_core import init_logger

from functions.student.other import get_list_of_classmates


logger = init_logger()


@dp.message_handler(text=back_to_menu_str, state=StudentStates.student)
async def all_shedule(message: types.Message):
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)


@dp.message_handler(text=all_schedule_str, state=StudentStates.student)
async def all_shedule_student(message: types.Message):
    await get_all_schedule(message, whose='general')


@dp.message_handler(text=group_schedule_str, state=StudentStates.student)
async def all_schedule_group(message: types.Message):
    await get_all_schedule(message, whose='general')


@dp.message_handler(text=personal_schedule_str, state=StudentStates.student)
async def all_schedule_personal(message: types.Message):
    await get_all_schedule(message, whose='personal')


@dp.message_handler(text=todays_shedule_str, state=StudentStates.student)
async def todays_shedule(message: types.Message):
    await get_todays_shedule(message, whose='general')


@dp.message_handler(text=next_lesson_str, state=StudentStates.student)
async def next_lesson(message: types.Message):
    await get_next_lesson(message, whose='general')


@dp.message_handler(text=tommorow_shedule_str, state=StudentStates.student)
async def tommorow_lesson(message: types.Message):
    await get_tommorow_lesson(message, whose='general')


@dp.message_handler(text=change_sched_str, state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=kb.change_sched_kb)


@dp.message_handler(text=add_lesson_str, state=StudentStates.student)
async def add_lesson_start(message: types.message):
    await message.answer('В какой день вы хотите добавить урок?', reply_markup=kb.days())
    await AddLesson.time.set()


@dp.message_handler(text=delete_lesson_str, state=StudentStates.student)
async def add_lesson_process_yes(message: types.message):
    await message.answer('Выберите день:', reply_markup=kb.days())
    await DeleteLesson.lesson.set()


@dp.message_handler(text=discover_free_time_str, state=StudentStates.student)
async def discover_free_time(message: types.message):
    await message.answer('Выберите день:', reply_markup=kb.days())
    await DiscoverFreeTime.output.set()


@dp.message_handler(state=DiscoverFreeTime.output)
async def output_free_time(message: types.message):
    await get_output_free_time(message, whose='general')


@dp.message_handler(commands=['deleteme'], state=StudentStates.student)
async def deleteme(message: types.Message):
    await delete_user(message, db)


@dp.message_handler(commands=['help'], state=StudentStates.student)
async def check_user(message: types.Message):
    await message.answer(help_user_text)


@dp.message_handler(commands=['time'], state=StudentStates.student)
async def next_lesson(message: types.Message):
    await message.answer(str(datetime.datetime.now()), reply_markup=kb.stud_kb)


@dp.message_handler(commands=['classmates'], state=StudentStates.student)
async def get_list_of_classmates(message: types.Message):
    await message.answer(await get_list_of_classmates(db, message.chat.id))


@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text='Я не понимаю что вы хотите', reply_markup=kb.stud_kb)

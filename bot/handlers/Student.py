import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboard as kb
from bot.states.states import StudentStates, AddLesson, DeleteLesson, DiscoverFreeTime, SetCaptainState
from bot.strings.messages import *
from bot.strings.commands import *
from functions.command import delete_user
from functions.student.change_schedule import check_privilege_whose

from functions.student.get_schedule import get_all_schedule, get_todays_shedule, get_next_lesson, get_tommorow_lesson, \
    get_output_free_time
from loader import dp, db
from logs.scripts.logging_core import init_logger

from functions.student.other import get_list_of_classmates, get_bio

logger = init_logger()


@dp.message_handler(text=back_to_menu_str, state=StudentStates.student)
async def back_to_menu(message: types.Message):
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)


@dp.message_handler(text=all_schedule_str, state=StudentStates.student)
async def all_shedule_student(message: types.Message):
    await get_all_schedule(message)


@dp.message_handler(text=todays_shedule_str, state=StudentStates.student)
async def todays_shedule(message: types.Message):
    await get_todays_shedule(message)


@dp.message_handler(text=next_lesson_str, state=StudentStates.student)
async def next_lesson(message: types.Message):
    await get_next_lesson(message)


@dp.message_handler(text=tommorow_shedule_str, state=StudentStates.student)
async def tommorow_lesson(message: types.Message):
    await get_tommorow_lesson(message)


@dp.message_handler(text=configuration_str, state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите изменить в настройках?', reply_markup=kb.configuration_kb)


@dp.message_handler(text=change_sched_str, state=StudentStates.student)
async def change_sched(message: types.message):
    if (await check_privilege_whose(message)) == 0:
        await message.answer('Что вы хотите сделать с расписанием?', reply_markup=kb.change_sched_kb)


@dp.message_handler(text=add_lesson_str, state=StudentStates.student)
async def add_lesson_start(message: types.message):
    if (await check_privilege_whose(message)) == 0:
        await message.answer('В какой день вы хотите добавить урок?', reply_markup=kb.days())
        await AddLesson.time.set()


@dp.message_handler(text=delete_lesson_str, state=StudentStates.student)
async def add_lesson_process_yes(message: types.message):
    if (await check_privilege_whose(message)) == 0:
        await message.answer('Выберите день:', reply_markup=kb.days())
        await DeleteLesson.lesson.set()


@dp.message_handler(text=discover_free_time_str, state=StudentStates.student)
async def discover_free_time(message: types.message):
    await message.answer('Выберите день:', reply_markup=kb.days())
    await DiscoverFreeTime.output.set()


@dp.message_handler(state=DiscoverFreeTime.output)
async def output_free_time(message: types.message):
    await get_output_free_time(message)


@dp.message_handler(commands=['bio'], state=StudentStates.student)
async def bio(message: types.Message):
    result = await get_bio(db, message.chat.id)
    await message.answer(result)


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
async def classmates(message: types.Message):
    await message.answer(await get_list_of_classmates(db, message.chat.id))


@dp.message_handler(commands=['captain_privilege'], state=StudentStates.student)
async def captain_privilege(message: types.Message):
    await message.answer('Введите пожалуйста ключ')
    await SetCaptainState.set.set()


@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text='Я не понимаю что вы хотите', reply_markup=kb.stud_kb)

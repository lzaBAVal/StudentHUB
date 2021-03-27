import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboard as kb
from bot.states.states import AnonStates, StudentStates, AddLesson, DeleteLesson, DiscoverFreeTime
from loader import dp, db
from logs.logging_core import init_logger
from schedule_json.change.change_sched import get_free_time
from schedule_json.output.get_schedule_object import get_sched_type, get_sched
from vars import WeekDays_RU, WeekDays_EN

logger = init_logger()


@dp.message_handler(text='Вернуться на главное меню', state=StudentStates.student)
async def all_shedule(message: types.Message):
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)


@dp.message_handler(text='Все расписание', state=StudentStates.student)
async def all_shedule(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=1)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Расписание на сегодня', state=StudentStates.student)
async def todays_shedule(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=2)
        if isinstance(resp, tuple):
            # await message.answer('Не удалось показать расписание, сообщите об этом админу.')
            await message.answer(resp[1])
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Cледующая пара', state=StudentStates.student)
async def next_lesson(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=3)
        if isinstance(resp, tuple):
            #await message.answer('Не удалось показать расписание, сообщите об этом админу.')
            await message.answer(resp[1])
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Расписание на завтра', state=StudentStates.student)
async def tommorow_lesson(message: types.Message):
    try:
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=4)
        if isinstance(resp, tuple):
            #await message.answer('Не удалось показать расписание, сообщите об этом админу.')
            await message.answer(resp[1])
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось показать расписание, сообщите об этом админу.')
    else:
        await message.answer(text=resp)


@dp.message_handler(text='Изменить расписание', state=StudentStates.student)
async def change_sched(message: types.message):
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=kb.change_sched_kb)


@dp.message_handler(text='Добавить урок', state=StudentStates.student)
async def add_lesson_start(message: types.message):
    await message.answer('В какой день вы хотите добавить урок?', reply_markup=kb.days())
    await AddLesson.time.set()


@dp.message_handler(text='Убрать урок', state=StudentStates.student)
async def add_lesson_process_yes(message: types.message):
    await message.answer('Выберите день:', reply_markup=kb.days())
    await DeleteLesson.lesson.set()


@dp.message_handler(text='Узнать свободное время', state=StudentStates.student)
async def discover_free_time(message: types.message, state: FSMContext):
    await message.answer('Выберите день:', reply_markup=kb.days())
    await DiscoverFreeTime.output.set()


@dp.message_handler(state=DiscoverFreeTime.output)
async def output_free_time(message: types.message, state: FSMContext):
    if message.text.lower() in WeekDays_RU:
        sched = await get_sched(message.chat.id)
        result = await get_free_time(message.text.lower(), sched)
        res = ''
        for i in range(len(result)):
            if i % 3 != 0:
                res += str(result[i]) + ' | '
            else: res += '\n| ' + str(result[i]) + ' | '
        await message.answer(str(res), reply_markup=kb.stud_kb)
        await StudentStates.student.set()
    else:
        await message.answer('Введите день недели!')

@dp.message_handler(commands=['deleteme'], state=StudentStates.student)
async def next_lesson(message: types.Message):
    try:
        await db.delete_account(message.chat.id)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Мне не удалось удалить ваш аккаунт, сообщите об этом админу')
    else:
        await AnonStates.anon.set()
        await message.answer('Ваш аккаунт был удален.', reply_markup=kb.anon_kb)


@dp.message_handler(commands=['time'], state=StudentStates.student)
async def next_lesson(message: types.Message):
    await message.answer(str(datetime.datetime.now()), reply_markup=kb.stud_kb)


@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text='На данный момент доступен только просмотр расписания!', reply_markup=kb.stud_kb)

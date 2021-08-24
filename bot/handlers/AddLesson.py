from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.functions.command import cancel
from bot.functions.student.add_lesson import add_lesson_time, add_lesson_lesson, add_lesson_teacher, \
    add_lesson_subgroup, \
    add_lesson_classroom, add_lesson_check, add_lesson_process
from bot.keyboard.keyboard import stud_kb
from bot.states.states import AddLesson
from log.logging_core import init_logger
from misc import dp

logger = init_logger()


# CANCEL ADD LESSON
# @dp.message_handler(lambda message: message.text.lower() == "отмена", state=AddLesson.states)
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state=AddLesson.states)
async def add_lesson_cancel(message: types.message, state: FSMContext):
    await message.answer(text='Добавьте урок заново', reply_markup=await stud_kb(state))
    await cancel(message, state)


# INPUT TIME FOR NEW LESSON
@dp.message_handler(state=AddLesson.time)
async def lesson_time(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_time(message, state, completed)


# INPUT NAME OF LESSON FOR NEW LESSON
@dp.message_handler(state=AddLesson.lesson)
async def lesson_lesson(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_lesson(message, state, completed)


# INPUT NAME OF TEACHER FOR NEW LESSON
@dp.message_handler(state=AddLesson.teacher)
async def lesson_teacher(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_teacher(message, state, completed)


# INPUT SUBGROUP FOR NEW LESSON
@dp.message_handler(state=AddLesson.subgroup)
async def lesson_subgroup(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_subgroup(message, state, completed)


# INPUT CLASSROOM FOR NEW LESSON
@dp.message_handler(state=AddLesson.classroom)
async def lesson_classroom(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_classroom(message, state, completed)


# CHECK DATA FOR NEW LESSON
@dp.message_handler(state=AddLesson.check)
async def lesson_check(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_check(message, state, completed)


# ACCEPT DATA
@dp.message_handler(Text(equals='Да', ignore_case=True), state=AddLesson.process)
async def lesson_process(message: types.message, state: FSMContext):
    if await add_lesson_process(message, state) == 1:
        await add_lesson_cancel(message, state)


# DISAGREE WITH DATA
@dp.message_handler(Text(equals='Нет', ignore_case=True), state=AddLesson.process)
async def add_lesson_process_no(message: types.message, state: FSMContext):
    await message.answer(text='Добавьте урок заново')
    await cancel(message, state)


# FINAL ADD LESSON
@dp.message_handler(state=AddLesson.final)
async def add_lesson_process_yes(message: types.message, state: FSMContext):
    await message.answer('Урок добавлен', reply_markup= await stud_kb(state))
    logger.info(f'User - {message.chat.id} has added new lesson in schedule')
    await cancel(message, state)

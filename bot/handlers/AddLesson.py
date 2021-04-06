from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboard as kb
from bot.states.states import StudentStates, AddLesson
from functions.student.add_lesson import add_lesson_time, add_lesson_lesson, add_lesson_teacher, add_lesson_subgroup, \
    add_lesson_classroom, add_lesson_check, add_lesson_process
from loader import dp


@dp.message_handler(lambda message: message.text.lower() == "отмена", state=AddLesson.states)
async def add_lesson_cancel(message: types.message, state: FSMContext):
    await message.answer(text='Добавьте урок заново', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=AddLesson.time)
async def lesson_time(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_time(message, state, completed)


@dp.message_handler(state=AddLesson.lesson)
async def lesson_lesson(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_lesson(message, state, completed)


@dp.message_handler(state=AddLesson.teacher)
async def lesson_teacher(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_teacher(message, state, completed)


@dp.message_handler(state=AddLesson.subgroup)
async def lesson_subgroup(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_subgroup(message, state, completed)


@dp.message_handler(state=AddLesson.classroom)
async def lesson_classroom(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_classroom(message, state, completed)


@dp.message_handler(state=AddLesson.check)
async def lesson_check(message: types.message, state: FSMContext, completed: bool = False):
    await add_lesson_check(message, state, completed)


@dp.message_handler(lambda message: message.text.lower() == "да", state=AddLesson.process)
async def lesson_process(message: types.message, state: FSMContext):
    await add_lesson_process(message, state)


@dp.message_handler(lambda message: message.text.lower() == "нет", state=AddLesson.process)
async def add_lesson_process_no(message: types.message, state: FSMContext):
    await message.answer(text='Добавьте урок заново')
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=AddLesson.final)
async def add_lesson_process_yes(message: types.message, state: FSMContext):
    await message.answer('Урок добавлен', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()

import base64

import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboard as kb
from bot.states.states import StudentStates, AddLesson
from loader import dp, db
from schedule_json.change.change_sched import add_lesson
from schedule_json.change.change_sched import get_free_time
from schedule_json.output.get_schedule_object import get_sched
from vars import WeekDays_RU, special_chars, special_chars_digit



@dp.message_handler(lambda message: message.text.lower() == "отмена", state=AddLesson.states)
async def add_lesson_cancel(message: types.message, state: FSMContext):
    await message.answer(text='Добавьте урок заново')
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=AddLesson.time)
async def add_lesson_time(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if message.text.lower() not in WeekDays_RU:
            await message.answer(text='Введите день недели!')
            return 0
        sched = await get_sched(message.chat.id)
        free_time = await get_free_time(message.text.lower(), sched)
        async with state.proxy() as data:
            data['day'] = message.text.lower()
            data['sched'] = sched
            data['free_time'] = free_time
    data = await state.get_data()
    await message.answer('Есть свободные часы в этот день: ', reply_markup=kb.free_time(data['free_time']))
    await AddLesson.next()


@dp.message_handler(state=AddLesson.lesson)
async def add_lesson_lesson(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        data = await state.get_data()
        if message.text not in data['free_time']:
            await message.answer(text='Введите время на которое хотите назначить урок!')
            await AddLesson.time.set()
            return 0

        async with state.proxy() as data:
            data['time'] = message.text
    await message.answer('Введите название урока')
    await AddLesson.next()


@dp.message_handler(state=AddLesson.teacher)
async def add_lesson_teacher(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 30 and not re.match(special_chars, message.text):
            async with state.proxy() as data:
                data['lesson'] = message.text
        else:
            await message.answer(text='Название урока должно быть меньше 30 символов и состоять только из букв и цифр!')
            await AddLesson.lesson.set()
            return 0
    await message.answer('Введите имя преподавателя')
    await AddLesson.next()


@dp.message_handler(state=AddLesson.subgroup)
async def add_lesson_subgroup(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 30 and not re.match(special_chars_digit, message.text):
            async with state.proxy() as data:
                data['teacher'] = message.text
        else:
            await message.answer(text='Имя преподавателя должно быть меньше 30 символов и состоять только из букв!')
            await AddLesson.teacher.set()
            return 0
    await message.answer('Введите подгруппу', reply_markup=kb.subgroup_kb)
    await AddLesson.next()


@dp.message_handler(state=AddLesson.classroom)
async def add_lesson_classroom(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if message.text.lower() == 'нет подгрупп' and not re.match(special_chars, message.text) or \
                re.match(r'\d', message.text):
            async with state.proxy() as data:
                data['subgroup'] = message.text
        else:
            await message.answer(text='Введите либо номер подгруппы либо укажите что подгрупп нет')
            await AddLesson.subgroup.set()
            return 0
    await message.answer('Введите номер кабинета или укажите что вы учитесь онлайн', reply_markup=kb.classroom_kb)
    await AddLesson.next()


@dp.message_handler(state=AddLesson.check)
async def add_lesson_check(message: types.message, state: FSMContext, completed: bool = False):
    if not completed:
        if len(message.text) <= 10 and not re.match(special_chars, message.text) or \
                message.text.lower() == 'онлайн':
            async with state.proxy() as data:
                data['classroom'] = message.text
            await message.answer(
                f"Проверьте данные: \n"
                f"День: {data['day']}\n\t"
                f"Время: {data['time']}\n\t"
                f"Урок: {data['lesson']}\n\t"
                f"Преподаватель: {data['teacher']}\n\t"
                f"Подгруппа: {data['subgroup']}\n\t"
                f"Кабинет: {data['classroom']}\n\n"
                f"Все верно?",
                reply_markup=kb.question_kb)
        else:
            await message.answer(
                text='Требуется наименование кабинет. Длина не более 10 символов или укажите что вы учитесь онлайн')
            await AddLesson.classroom.set()
            return 0

    await AddLesson.next()


@dp.message_handler(lambda message: message.text.lower() == "да", state=AddLesson.process)
async def add_lesson_process(message: types.message, state: FSMContext):
    data = await state.get_data()
    sched = await add_lesson(sched=data['sched'], day=WeekDays_RU.index(data['day']), complex_time=data['time'],
                             classroom=data['classroom'], name_lesson=data['lesson'], teacher=data['teacher'])
    sched = str(base64.b64encode(str(sched.dict()).encode('utf-8')))[2:-1]
    await db.update_group_sched(sched, message.chat.id)
    await AddLesson.next()
    await message.answer('Идет процесс занесения урока в базу! Для завершения тыкните на котика',
                         reply_markup=kb.cat_kb)


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

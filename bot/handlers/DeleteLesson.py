from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboard as kb
from bot.states.states import StudentStates, DeleteLesson
from loader import dp
from logs.logging_core import init_logger
from schedule_json.change.change_sched import delete_lesson
from schedule_json.change.change_sched import get_lessons_time
from schedule_json.output.get_schedule_object import get_sched, update_sched

logger = init_logger()


@dp.message_handler(lambda message: message.text.lower() == "отмена", state=DeleteLesson.states)
async def cancel_delete_lesson(message: types.message, state: FSMContext):
    await message.answer('Вы прервали процесс удаления', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=DeleteLesson.lesson)
async def delete_lesson_lesson(message: types.message, state: FSMContext):
    sched = await get_sched(message.chat.id, 'sched_user')
    async with state.proxy() as data:
        data['day'] = message.text.lower()
        data['sched'] = sched
    lessons_time = await get_lessons_time(data['day'], sched)
    if isinstance(lessons_time, tuple):
        await message.answer(lessons_time[1] + '\nВы в главном меню', reply_markup=kb.stud_kb)
        await state.finish()
        await StudentStates.student.set()
        return 0

    await message.answer('Какой предмет вы желаете удалить?', reply_markup=kb.free_time(lessons_time))
    await DeleteLesson.next()


@dp.message_handler(state=DeleteLesson.check)
async def delete_lesson_check(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['deletelesson'] = message.text
    await message.answer('Вы уверены что хотите удалить "' + data['deletelesson'] + '" из расписания?',
                         reply_markup=kb.question_kb)
    await DeleteLesson.next()


@dp.message_handler(lambda message: message.text.lower() == "да", state=DeleteLesson.process)
async def delete_lesson_check(message: types.message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Идет процесс удаления записи из расписания... \n'
                         'Тыкните на котика чтобы завержить процесс удаления',
                         reply_markup=kb.cat_kb)
    new_sched = delete_lesson(data['sched'], data['deletelesson'], day=data['day'])
    if new_sched == -1:
        await message.answer('В этот день нет пар!\nВы в главном меню', reply_markup=kb.stud_kb)
        await state.finish()
        await StudentStates.student.set()
        return 0
    # await db.update_group_sched(new_sched, message.chat.id)
    await update_sched(message.chat.id, new_sched, 'sched_user')
    await DeleteLesson.next()


@dp.message_handler(lambda message: message.text.lower() == "нет", state=DeleteLesson.process)
async def delete_lesson_check(message: types.message, state: FSMContext):
    await message.answer('Вы прервали процесс удаления', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=DeleteLesson.final)
async def delete_lesson_check(message: types.message, state: FSMContext):
    await message.answer('Вы удалили запись из расписания', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.states.states import CaptainSchedule, StudentStates
from bot import keyboard as kb
from loader import dp


@dp.message_handler(text='Изменить расписание', state=CaptainSchedule.select)
async def select_sched(message: types.Message):
    await message.answer('Чье расписание вы хотите изменить?', reply_markup=kb.which_sched_kb)


@dp.message_handler(text='Личное расписание', state=CaptainSchedule.select)
async def change_sched(message: types.Message):
    StudentStates.student.set()
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=kb.change_sched_kb)


@dp.message_handler(text='Расписание группы', state=CaptainSchedule.select)
async def change_sched(message: types.Message, state: FSMContext):
    await state.set_data({'whose': 'general'})
    await message.answer('Что вы хотите сделать с расписанием?', reply_markup=kb.change_sched_kb)
    await StudentStates.student.set()
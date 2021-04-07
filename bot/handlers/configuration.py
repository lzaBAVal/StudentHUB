from aiogram.dispatcher import FSMContext

import bot.keyboard as kb
from functions.whois import whois_str
from logs.logging_core import init_logger

from aiogram import types

from bot.states.states import StudentStates, ConfigWhoseScheduleState
from bot.strings.commands import whose_schedule_str, back_to_menu_str, personal_schedule_str, group_schedule_str
from loader import dp, db

logger = init_logger()


@dp.message_handler(commands=['/cancel'], state=ConfigWhoseScheduleState.states)
async def cancel_config(message: types.message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(text=back_to_menu_str, state=ConfigWhoseScheduleState.states)
async def cancel_config(message: types.message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(text=whose_schedule_str, state=StudentStates.student)
async def select_schedule(message: types.message):
    try:
        whose = (await db.get_whose_sched(message.chat.id))[0]['whose_schedule']
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Что то не так, сообщите об этом админу', reply_markup=kb.stud_kb)
    else:
        whose = whois_str(whose)
        await message.answer(f'На текущий момент вы видите "{whose}"\n'
                             f'Если хотите использовать другое расписание (всего имеется групповое, персональное) '
                             f'нажмите на одну из кнопок ниже',
                             reply_markup=kb.select_whose_schedule_kb)
        await ConfigWhoseScheduleState.select.set()


@dp.message_handler(text=personal_schedule_str, state=ConfigWhoseScheduleState.select)
async def select_personal_schedule(message: types.message, state: FSMContext):
    try:
        await db.update_whose_schedule('personal', message.chat.id)
    except Exception as exc:
        logger.exception(exc)
        message.answer('Не удалось изменить расписание по умолчанию')
        await cancel_config(message, state)
    await message.answer('Теперь вы используете ваше персональное расписание по умолчанию')
    await cancel_config(message, state)


@dp.message_handler(text=group_schedule_str, state=ConfigWhoseScheduleState.select)
async def select_group_schedule(message: types.message, state: FSMContext):
    try:
        await db.update_whose_schedule('general', message.chat.id)
    except Exception as exc:
        logger.exception(exc)
        message.answer('Не удалось изменить расписание по умолчанию')
        await cancel_config(message, state)
    await message.answer('Теперь вы используете расписание группы по умолчанию')
    await cancel_config(message, state)

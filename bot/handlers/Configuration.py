from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.keyboard.keyboard import stud_kb, select_whose_schedule_kb, sched_parts_kb, \
    update_sched_parts
from functions.command import cancel
from functions.whois import whois_str
from models import Student
from utils.log.logging_core import init_logger

from aiogram import types

from bot.states.states import StudentStates, ConfigWhoseScheduleState, ConfigureScheduleParts
from bot.strings.commands import whose_schedule_str, back_to_menu_str, personal_schedule_str, group_schedule_str, \
    finish_configuration_str
from misc import dp

logger = init_logger()


# SELECT MAIN SCHEDULE
@dp.message_handler(text=whose_schedule_str, state=StudentStates.student)
async def select_schedule(message: types.message):
    try:
        whose = await Student.filter(chat_id=message.chat.id).values_list('whose_schedule')
        whose = whose[0][0]
        print(whose)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Что то не так, сообщите об этом админу', reply_markup=stud_kb())
    else:
        whose = whois_str(whose)
        await message.answer(f'На текущий момент вы видите "{whose}"\n'
                             f'Если хотите использовать другое расписание (всего имеется групповое, персональное) '
                             f'нажмите на одну из кнопок ниже',
                             reply_markup=select_whose_schedule_kb)
        await ConfigWhoseScheduleState.select.set()


# CANCEL CONFIGURE SELECT MAIN SCHEDULE
@dp.message_handler(text=back_to_menu_str, state=ConfigWhoseScheduleState.states)
async def cancel_config(message: types.message, state: FSMContext):
    await cancel(message, state)


# SELECT PERSONAL SCHEDULE
@dp.message_handler(text=personal_schedule_str, state=ConfigWhoseScheduleState.select)
async def select_personal_schedule(message: types.message, state: FSMContext):
    try:
        await Student.filter(chat_id=message.chat.id).update(whose_schedule='p')
    except Exception as exc:
        logger.exception(exc)
        message.answer('Не удалось изменить расписание по умолчанию')
        await cancel_config(message, state)
    await message.answer('Теперь вы используете ваше персональное расписание по умолчанию')
    await cancel_config(message, state)


# SELECT GROUP SCHEDULE
@dp.message_handler(text=group_schedule_str, state=ConfigWhoseScheduleState.select)
async def select_group_schedule(message: types.message, state: FSMContext):
    try:
        await Student.filter(chat_id=message.chat.id).update(whose_schedule='g')
    except Exception as exc:
        logger.exception(exc)
        message.answer('Не удалось изменить расписание по умолчанию')
        await cancel_config(message, state)
    await message.answer('Теперь вы используете расписание группы по умолчанию')
    await cancel_config(message, state)


# CONFIGURE SCHEDULES OUTPUT FOR STUDENT
@dp.message_handler(text='Настройка вывода расписания', state=StudentStates.student)
async def configure_sched_parts(message: types.message, state: FSMContext):
    parts = await Student.filter(chat_id=message.chat.id).values_list('sched_parts')
    parts = parts[0][0]
    async with state.proxy() as data:
        data['parts'] = parts
    await message.answer('С помощью данной настрйоки вы можете изменить вывод расписания под себя. Нажимайте на кнопки '
                         'ниже чтобы выводить или не выводить те или иные элементы расписания.\n'
                         'Данная настройка будет работать для всех выводов, кроме "полного" расписания',
                         reply_markup=sched_parts_kb(data['parts']))
    await ConfigureScheduleParts.choose_part.set()


# CHOOSE SCHEDULES PARTS
@dp.message_handler(Text(equals=finish_configuration_str, ignore_case=True), state=ConfigureScheduleParts.choose_part)
async def configure_sched_parts(message: types.message, state: FSMContext):
    await message.answer('Вы закончили настройку', reply_markup=stud_kb())
    await state.reset_data()
    await StudentStates.student.set()


# CHOOSE SCHEDULES PARTS
@dp.message_handler(state=ConfigureScheduleParts.choose_part)
async def configure_sched_parts(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        pass
    result = update_sched_parts(data['parts'], message.text)
    print(f'result: {result}')
    if result is None:
        await message.answer('Вы вводите что-то не понятное', reply_markup=sched_parts_kb(data['parts']))
        return 0
    await Student.filter(chat_id=message.chat.id).update(sched_parts=result)
    async with state.proxy() as data:
        data['parts'] = result
    await message.answer(result, reply_markup=sched_parts_kb(data['parts']))

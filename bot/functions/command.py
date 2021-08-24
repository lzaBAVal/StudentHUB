from aiogram import types
from aiogram.dispatcher import FSMContext

from DB.models import Student
from bot.keyboard.keyboard import stud_kb, anon_kb
from bot.states.states import AnonStates, StudentStates
from log.logging_core import init_logger

logger = init_logger()


async def cancel(message: types.Message, state: FSMContext):
    await StudentStates.student.set()
    await message.answer('Вы в главном меню', reply_markup=await stud_kb(state))


async def delete_user(message: types.Message):
    try:
        await Student.filter(chat_id=message.chat.id).delete()
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось удалить ваш аккаунт, сообщите об этом администратору')
    else:
        await AnonStates.anon.set()
        await message.answer('Ваш аккаунт был удален.', reply_markup=anon_kb)
        logger.info(f'User - {message.chat.id} delete account')
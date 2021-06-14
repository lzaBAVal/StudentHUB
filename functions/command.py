from aiogram.dispatcher import FSMContext

from aiogram import types

from bot.keyboard.keyboard import stud_kb, anon_kb
from bot.states.states import AnonStates, StudentStates
from models import Student
from utils.log.logging_core import init_logger


logger = init_logger()


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await StudentStates.student.set()
    await message.answer('Вы в главном меню', reply_markup=stud_kb())


async def delete_user(message: types.Message):
    try:
        await Student.filter(chat_id=message.chat.id).delete()
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Мне не удалось удалить ваш аккаунт, сообщите об этом админу')
    else:
        await AnonStates.anon.set()
        await message.answer('Ваш аккаунт был удален.', reply_markup=anon_kb)
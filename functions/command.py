from aiogram.dispatcher import FSMContext

import bot.keyboard as kb

from aiogram import types

from bot.states.states import AnonStates, StudentStates
from logs.scripts.logging_core import init_logger


logger = init_logger()


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await StudentStates.student.set()
    await message.answer('Вы в главном меню', reply_markup=kb.stud_kb)


async def delete_user(message: types.Message, db):
    try:
        await db.delete_account(message.chat.id)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Мне не удалось удалить ваш аккаунт, сообщите об этом админу')
    else:
        await AnonStates.anon.set()
        await message.answer('Ваш аккаунт был удален.', reply_markup=kb.anon_kb)


async def identify_user(message: types.Message, db):
    try:
        if not (await db.check_user(message.chat.id)):
            await AnonStates.anon.set()
            await message.answer(text='Анон.', reply_markup=kb.anon_kb)
        else:
            await StudentStates.student.set()
            await message.answer(text='Повторите ваш запрос', reply_markup=kb.stud_kb)
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)
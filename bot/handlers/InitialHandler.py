from aiogram.dispatcher import FSMContext

from bot.keyboard.keyboard import anon_kb
from bot.strings.messages import *

from aiogram import types

from bot.states.states import AnonStates, StudentStates
from misc import dp
from models import Student
from utils.log.logging_core import init_logger

logger = init_logger()

# NONE ------------------------------------------------------------------------
'''
@dp.message_handler(state=None)
async def state_none(message: types.Message):
    await message.answer('Упс, что то пошло не так.')
    logger.warn(f'Student - {0}. STATE NONE!')
'''


@dp.message_handler(state=None)
async def def_user(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        user = await Student.filter(id_chat=message.chat.id).all()
        if not user[0]:
            await AnonStates.anon.set()
        else:
            await StudentStates.student.set()
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Что то пошло не так! Ошибка', reply_markup=anon_kb)


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await AnonStates.anon.set()
    await message.answer(text=start_text, reply_markup=anon_kb)


# ALL ------------------------------------------------------------------------

@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)

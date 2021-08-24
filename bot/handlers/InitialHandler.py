from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from DB.models import Student
from bot.keyboard.keyboard import anon_kb, cancel_str, stud_kb
from bot.states.states import AnonStates, StudentStates
from bot.strings.messages import *
from log.logging_core import init_logger
from misc import dp

logger = init_logger()

# NONE ------------------------------------------------------------------------
'''
@dp.message_handler(state=None)
async def state_none(message: types.Message):
    await message.answer('Упс, что то пошло не так.')
    logger.warn(f'Student - {0}. STATE NONE!')
'''


@dp.message_handler(commands='cancel', state='*')
async def cancel_all(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись в главное меню')
    await def_user(message, state)
    await state.reset_data()


@dp.message_handler(state=None)
async def def_user(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        user = await Student.filter(chat_id=message.chat.id).all()
        print(user)
        if not user:
            await AnonStates.anon.set()
        else:
            await StudentStates.student.set()
            # await message.answer('Вы в главном меню', reply_markup=await stud_kb(state))
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Что то пошло не так! Ошибка', reply_markup=anon_kb)


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await AnonStates.anon.set()
    await message.answer(text=start_text, reply_markup=anon_kb)
    logger.info(f'User - {message.chat.id} entered')


# ALL ------------------------------------------------------------------------

@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)

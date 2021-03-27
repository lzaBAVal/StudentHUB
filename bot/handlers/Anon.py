from aiogram import types

from bot import keyboard as kb
from bot.states.states import AnonStates, RegistrationStates
from loader import dp
from logs.logging_core import init_logger


logger = init_logger()


@dp.message_handler(state=AnonStates.anon, text='Регистрация')
async def reg_start(message: types.Message):
    await RegistrationStates.name.set()
    await message.answer(text='Введите ваше имя', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AnonStates.anon)
async def anon_message(message: types.Message):
    await message.answer(
        text='На данный момент я вас не знаю, пройдите регистрацию чтобы получить доступ к моему функционалу',
        reply_markup=kb.anon_kb)

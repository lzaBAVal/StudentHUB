from aiogram import types

from bot import keyboard as kb
from bot.states.states import AnonStates, RegistrationStates, StudentStates
from bot.strings.messages import help_anon_str
from functions.command import identify_user
from loader import dp, db
from logs.logging_core import init_logger


logger = init_logger()


@dp.message_handler(state=AnonStates.anon, commands=['help'])
async def help_anon(message: types.Message):
    await message.answer(text=help_anon_str)


@dp.message_handler(state=AnonStates.anon, commands=['check'])
async def identify(message: types.Message):
    await identify_user(message, db)


@dp.message_handler(state=AnonStates.anon, text='Регистрация')
async def reg_start(message: types.Message):
    await message.answer(text='Введите ваше имя', reply_markup=types.ReplyKeyboardRemove())
    await RegistrationStates.name.set()


@dp.message_handler(state=AnonStates.anon)
async def anon_message(message: types.Message):
    await message.answer(
        text='На данный момент я вас не знаю, пройдите регистрацию чтобы получить доступ к моему функционалу',
        reply_markup=kb.anon_kb)

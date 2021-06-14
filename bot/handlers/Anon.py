from aiogram import types

from bot.keyboard.keyboard import anon_kb
from bot.states.states import AnonStates, RegistrationStates
from bot.strings.messages import help_anon_str, start_text
from loader import db
from misc import dp
from utils.log.logging_core import init_logger


logger = init_logger()


# START FOR ANON
@dp.message_handler(commands=['start'], state=AnonStates.anon)
async def start(message: types.Message):
    await message.answer(text=start_text, reply_markup=anon_kb)


# GET HELP FOR ANON
@dp.message_handler(state=AnonStates.anon, commands=['help'])
async def help_anon(message: types.Message):
    await message.answer(text=help_anon_str)


# REGISTRATION FOR STUDENT INITIAL
@dp.message_handler(state=AnonStates.anon,
                    text='Регистрация')
async def reg_start(message: types.Message):
    await message.answer(text='Введите ваше имя', reply_markup=types.ReplyKeyboardRemove())
    await RegistrationStates.name.set()


# OTHER COMMAND FOR ANON
@dp.message_handler(state=AnonStates.anon)
async def anon_message(message: types.Message):
    await message.answer(
        text='На данный момент я вас не знаю, пройдите регистрацию чтобы получить доступ к моему функционалу',
        reply_markup=anon_kb)

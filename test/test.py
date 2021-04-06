import logging

import aiogram.utils.markdown as md

from logs.logging_core import init_logger
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1533907938:AAFdL_sf1pH_FwNZqxihjX7JqDUcOk5bXKE'

logger = init_logger()

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Hi there! What's your name?")


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("How old are you?")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(age=int(message.text))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")
    markup.add("Other")
    await message.reply("What is your gender?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Bad gender name. Choose your gender from the keyboard.")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Hi! Nice to meet you,', md.bold(data['name'])),
                md.text('Age:', md.code(data['age'])),
                md.text('Gender:', data['gender']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()


if __name__ == '__main__':
    logging.info('Привет')
    logging.info('Привет'.encode('ascii', errors='backslashreplace'))
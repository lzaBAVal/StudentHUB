from bot.strings.messages import *

from aiogram import types

from bot import keyboard as kb
from bot.states.states import AnonStates, StudentStates
from loader import dp, db
from logs.scripts.logging_core import init_logger

logger = init_logger()


# NONE ------------------------------------------------------------------------
@dp.message_handler(state=None)
async def state_none(message: types.Message):
    await message.answer('Упс, что то пошло не так.')
    logger.warn(f'User - {0}. STATE NONE!')


@dp.message_handler(state=None)
async def def_user(message: types.Message):
    try:
        if not (await db.check_user(message.chat.id)):
            await AnonStates.anon.set()
        else:
            await StudentStates.student.set()
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)


@dp.message_handler(commands=['start'], state=AnonStates.anon)
async def start(message: types.Message):
    await AnonState.anon.set()
    await message.answer(text=start_text, reply_markup=kb.anon_kb)


# ALL ------------------------------------------------------------------------

@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)


'''
@dp.message_handler(commands=['setstate'])
async def process_setstate(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)
'''

'''
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
'''

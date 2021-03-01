import logging
import keyboard as kb
import schedule_parce.parcing as parce
import aiogram.utils.markdown as md
from DB import pgsql_requests as pg_req, pgsql_conn

from find_group import search_shed_using_group
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from auxiliary.utils import AnonStates, RegistrationStates, StudentStates


# ----------------------------------------------------------------------------------------------------
class Grp(StatesGroup):
    name = State()
    inst = State()


# ----------------------------------------------------------------------------------------------------

API_TOKEN = '1533907938:AAFdL_sf1pH_FwNZqxihjX7JqDUcOk5bXKE'

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_id = 690976128


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await AnonStates.anon.set()
    await message.answer(text='Привет, чел! Я тестовый бот.', reply_markup=kb.anon_kb)


@dp.message_handler(state=AnonStates.anon, text='Регистрация')
async def reg_start(message: types.Message):
    await RegistrationStates.name.set()
    await message.answer(text='Введите ваше имя', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AnonStates.anon)
async def reg_start(message: types.Message):
    await message.answer(text='Что тебе анон?', reply_markup=kb.anon_kb)


@dp.message_handler(state=RegistrationStates.name)
async def reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RegistrationStates.next()
    await message.answer(text='Введите вашу фамилию')


@dp.message_handler(state=RegistrationStates.surname)
async def reg_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await RegistrationStates.next()
    await message.answer(text='Введите наименование вашей группы')


@dp.message_handler(state=RegistrationStates.find_group)
async def reg_group(message: types.Message, state: FSMContext):
    group = search_shed_using_group(message.text)
    if type(group) == str:
        async with state.proxy() as data:
            data['group'] = search_shed_using_group(message.text)
        await message.answer(text='Проверьте все ваши данные. Все правильно?')
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Имя,', data['name']),
                md.text('Фамилия:', data['surname']),
                md.text('Группа:', data['group']),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        await RegistrationStates.next()
    elif type(group) == list:
        new_btn = kb.createButtons(group)
        await message.answer(text='Найденные группы', reply_markup=new_btn)
        await RegistrationStates.find_group.set()
    else:
        await message.answer(text='Произошло неведомое, пиши разрабу! Error')
        await state.finish()
        await AnonStates.anon.set()


@dp.message_handler(state=RegistrationStates.final, text='Да')
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Все отлично! Теперь вы зарегестрированы.', reply_markup=kb.greet_kb)
    await pgsql_conn.pgsql_conn(pg_req.add_user(message.chat.id, state.proxy()['name'], state.proxy()['surname'], state.proxy()['group'], 1))
    await state.finish()
    await StudentStates.student.set()

@dp.message_handler(state=RegistrationStates.final, text='Нет')
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Пройдите регистрацию заново!')
    await state.finish()
    await AnonStates.anon.set()


@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)


@dp.message_handler(text='Все расписание', state=StudentStates.student)
async def all_shedule(message: types.Message):
    await message.answer(text=parce.all_shedule())


@dp.message_handler(text='Cледующая пара', state=StudentStates.student)
async def next_leson(message: types.Message):
    await message.answer(text=parce.current_lesson())


@dp.message_handler(text='Расписание на сегодня', state=StudentStates.student)
async def todays_shedule(message: types.Message):
    await message.answer(text=parce.schedule_for_today())


@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text=message.text, reply_markup=kb.greet_kb)


# @dp.message_handler(commands=['linebut'])
# async def inlinebutton(message: types.Message):
#    await message.reply('Первая инлайн кнопка', reply_markup=kb.inline_kb1)


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


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.message_handler(commands=['help'], state='*')
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice test', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

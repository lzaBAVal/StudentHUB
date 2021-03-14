import aiogram.utils.markdown as md

from logging_core import init_logger
from bot import keyboard as kb
from functions.find_group import group_search
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from loader import dp, db, bot
from aiogram import types
from bot.states.states import AnonStates, RegistrationStates, StudentStates
from schedule.output.get_schedule_object import get_sched
from schedule.harvest.harvest_main import harvest_groups, harvest_groups_arhit_sched

logger = init_logger()

@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await AnonStates.anon.set()
    await message.answer(text='Привет, чел! Я тестовый бот.', reply_markup=kb.anon_kb)


@dp.message_handler(state=AnonStates.anon, text='Регистрация')
async def reg_start(message: types.Message):
    await RegistrationStates.name.set()
    await message.answer(text='Введите ваше имя', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AnonStates.anon)
async def anon_message(message: types.Message):
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
    await message.answer(text='Введите наименование вашей группы. Вы должны ввести строку вида \'сиб 19 6\'')


@dp.message_handler(state=RegistrationStates.find_group)
async def search_group(message: types.Message, state: FSMContext):
    result = await group_search(message.text)
    if result == -1:
        await message.answer(text='Не могу разобрать что вы пишите, попробуйте снова. Напомню, вводить наименование группы должно быть такого формата - "cиб 19 6"')
    else:
        comp_match, match, other_match = result
        if comp_match:
            kboard = kb.createButtons(comp_match)
            await message.answer(text='Это наименование твоей группы?', reply_markup=kboard)
            #await RegistrationStates.next()
        elif match:
            kboard = kb.createButtons(match)
            await message.answer(text='Не найденно точной группы. Твоя группа есть в этом списке?', reply_markup=kboard)
            #await RegistrationStates.next()
        elif other_match:
            kboard = kb.createButtons(other_match)
            await message.answer(text='Я не нашел ничего похожего. Только это', reply_markup=kboard)
            #await RegistrationStates.next()
        else:
            await message.answer(text='Вашей группы у меня нет. Напишите разработчику, он все исправит')
            #await RegistrationStates.find_group.set()


@dp.message_handler(state=RegistrationStates.accept_all_data)
async def accept_all_data(message: types.Message, state: FSMContext):
    group_id = await db.get_group_id(message.text)
    group_id = dict(group_id)['id_inc']
    async with state.proxy() as data:
        data['group_name'] = message.text
        data['group_id'] = group_id
    await message.answer(text='Проверьте все ваши данные. Все правильно?', reply_markup=kb.question_kb)
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Имя,', data['name']),
            md.text('Фамилия:', data['surname']),
            md.text('Группа:', data['group_name']),
            sep='\n',
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.insert_sql, text='Да')
async def reg_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await db.add_user(message.chat.id, data['name'], data['surname'], str(data['group_id']))
    except Exception as e:
        print(e)
        await message.answer(text='Произошла ошибка, обратитесь к разработчику)', reply_markup=kb.anon_kb)
        await state.finish()
        await AnonStates.anon.set()
    await message.answer(text='Идет процесс регистрации...\n для завершения тыкни на котика)', reply_markup=kb.cat_kb)
    await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.final)
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Все отлично! Теперь вы зарегестрированы.', reply_markup=kb.greet_kb)
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=RegistrationStates.insert_sql, text='Нет')
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Пройдите регистрацию заново!')
    await state.finish()
    await AnonStates.anon.set()


@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)

'''
# This block of code is a test harvest the groups and schedules 

@dp.message_handler(commands=['update1'], state='*')
async def chat_id(message: types.Message):
    await harvest_groups(db)


@dp.message_handler(commands=['update2'], state='*')
async def chat_id(message: types.Message):
    await harvest_groups_arhit_sched(db)
'''

@dp.message_handler(text='Все расписание', state=StudentStates.student)
async def all_shedule(message: types.Message):
    print('it\'s works')
    resp = await get_sched(id_chat=message.chat.id, type_of_shed=1)
    await message.answer(text=resp)


@dp.message_handler(text='Cледующая пара', state=StudentStates.student)
async def next_lesson(message: types.Message):
    resp = await get_sched(id_chat=message.chat.id, type_of_shed=3)
    await message.answer(text=resp)


@dp.message_handler(text='Расписание на сегодня', state=StudentStates.student)
async def todays_shedule(message: types.Message):
    resp = await get_sched(id_chat=message.chat.id, type_of_shed=2)
    await message.answer(text=resp)


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

@dp.message_handler(state=StudentStates.student)
async def get_menu(message: types.Message):
    await message.answer(text=message.text, reply_markup=kb.greet_kb)

@dp.message_handler(state=None)
async def def_user(message: types.Message):
    try:
        if (await db.check_user(message.chat.id)) == []:
            await AnonStates.anon.set()
            await message.answer(text='Привет Анон', reply_markup=kb.anon_kb)
        else:
            await StudentStates.student.set()
    except Exception as e:
        await AnonStates.anon.set()
        await message.answer(text='Привет Анон', reply_markup=kb.anon_kb)
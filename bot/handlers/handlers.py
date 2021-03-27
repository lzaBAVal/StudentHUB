from aiogram import types

from bot import keyboard as kb
from bot.states.states import AnonStates, StudentStates, TesterState
from loader import dp, db
from logs.logging_core import init_logger

from schedule_json.harvest.harvest_main import harvest_spec_group, harvest_spec_arhit_sched

logger = init_logger()

# NONE
'''
@dp.register_message_handler(State=None)
async def def_user(message: types.Message, state: FSMContext):
    try:
        if not (await db.check_user(message.chat.id)):
            await AnonStates.anon.set()
            await state.set_state(AnonStates.anon)
            print('Anon_check')
            # await message.answer(text='Анон.', reply_markup=kb.anon_kb)
        else:
            await StudentStates.student.set()
            await state.set_state(StudentStates.student)
            await state.reset_state()
            print('Student_check')
            # await message.answer(text='Повторите ваш запрос', reply_markup=kb.stud_kb)
    except Exception as exc:
        logger.exception(exc)
        await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)
    print('Handler? check')
    #raise SkipHandler()
'''

@dp.message_handler(state=None)
async def def_user(message: types.Message):
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


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await TesterState.tester.set()
    await message.answer(text='Привет, студент! Я бот \nНа данный момент идет тестовый период моей работы.\
    \nЯ могу ошибаться, тормозить в общем работать не так как нужно)\
    \nЕсли ты хочешь пользоваться моим функционалом или помочь мне, тогда тебе нужен ключик для входа\
    \nЕго можно взять у моего разработчика или админов \
    \nЕсли уже есть ключик то жмакай на кнопку ввести ключ и вводи его)\
    \nРазработчик будет очень рад если ты будешь отправлять ему замечания по поводу моей работы!',
                         reply_markup=kb.tester_kb)


# ALL ------------------------------------------------------------------------

@dp.message_handler(commands=['update_spec_group'], state='*')
async def update_spec_group(message: types.Message):
    await harvest_spec_group(db)


@dp.message_handler(commands=['update_spec_sched'], state='*')
async def update_spec_sched(message: types.Message):
    await harvest_spec_arhit_sched(db)


@dp.message_handler(commands=['id'], state='*')
async def chat_id(message: types.Message):
    await message.answer(text=message.chat.id)


'''
# This block of code is a test harvest the groups and schedules 

@dp.message_handler(commands=['update1'], state='*')
async def id_chat(message: types.Message):
    await harvest_groups(db)


@dp.message_handler(commands=['update2'], state='*')
async def id_chat(message: types.Message):
    await harvest_arhit_sched(db)
'''

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

'''
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
'''

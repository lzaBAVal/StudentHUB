import aiogram.utils.markdown as md

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from bot.keyboard.keyboard import anon_kb, register_kb, createButtons, question_kb, cat_kb, stud_kb
from bot.states.states import AnonStates, RegistrationStates, StudentStates

from functions.other.find_group import group_search

from loader import db, bot
from misc import dp
from models import Group, Student
from utils.log.logging_core import init_logger, log_encode

logger = init_logger()


# CANCEL REGISTRATION
@dp.message_handler(Text(equals='отмена', ignore_case=True), state=RegistrationStates)
async def reg_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await AnonStates.anon.set()
    await message.answer('Регистрация отменена', reply_markup=anon_kb)


# INPUT NAME FOR REGISTRATION
@dp.message_handler(state=RegistrationStates.name)
async def reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(text='Введите вашу фамилию', reply_markup=register_kb)
    await RegistrationStates.next()


# INPUT SURNAME FOR REGISTRATION
@dp.message_handler(state=RegistrationStates.surname)
async def reg_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await message.answer(text='Введите наименование вашей группы. Вы должны ввести строку вида \'сиб 19 6\'')
    await RegistrationStates.next()


# INPUT GROUP FOR REGISTRATION
@dp.message_handler(state=RegistrationStates.find_group)
async def search_group(message: types.Message):
    result = await group_search(message.text)
    logger.info(f'User - {0} is finding himself group - '.format(message.chat.id) +
                log_encode(message.text.encode('utf-8')))
    if result == -1:
        await message.answer(
            text='Не могу разобрать что вы пишите, попробуйте снова. Напомню, наименование группы должно быть такого '
                 'формата - "cиб 19 6"')
    else:
        comp_match, match, other_match = result
        if comp_match:
            kboard = createButtons(comp_match)
            await message.answer(text='Это наименование вашей группы?', reply_markup=kboard)
            await RegistrationStates.next()
        elif match:
            kboard = createButtons(match)
            await message.answer(text='Не найдено точное наименование вашей группы. Ваша группа есть в этом списке?',
                                 reply_markup=kboard)
            # await RegistrationStates.next()
        elif other_match:
            kboard = createButtons(other_match)
            await message.answer(
                text='Я не нашел ничего похожего. Посмотрите список групп который я вам предоставил. Возможно там '
                     'будет то что вам нужно',
                reply_markup=kboard)
            # await RegistrationStates.next()
        else:
            await message.answer(
                text='Вашей группы у меня нет. Если вы уверены что верно вводите название группы, напишите об этом '
                     'разработчику, он вам поможет',
                reply_markup=anon_kb)
            await AnonStates.anon.set()


# CHECK ALL INTRODUCED DATA
@dp.message_handler(state=RegistrationStates.accept_all_data)
async def accept_all_data(message: types.Message, state: FSMContext):
    try:
        group_id = await Group.filter(group_name=message.text).values_list('id')
        # group_id = await db.get_group_id(message.text)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('ERROR: произошла ошибка. Регистрация отменена')
        await state.finish()
        await AnonStates.anon.set()
    else:
        group_id = group_id[0][0]
        async with state.proxy() as data:
            data['group_name'] = message.text
            data['group_id'] = group_id
        await message.answer(text='Проверьте все ваши данные. Все правильно?', reply_markup=question_kb)
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


# USER CHECKED ALL DATA. ACCEPTED
@dp.message_handler(Text(equals='да', ignore_case=True), state=RegistrationStates.insert_sql)
async def reg_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lock = await Group.filter(id=data['group_id']).values_list('lock')
    if lock[0][0] is True:
        await message.answer(text='Вход в данную группу закрыт старостой этой группы, '
                                  'обратитесь к нему, чтобы он открыл её',
                             reply_markup=anon_kb)
        await state.finish()
        await AnonStates.anon.set()
    try:
        await Student.create(chat_id=int(message.chat.id),
                             name=str(data['name']),
                             surname=str(data['surname']),
                             group_id=int(data['group_id']),
                             group_name=str(data['group_name']),
                             sched_parts='11111',
                             whose_schedule='g',
                             ban=False,
                             privilege='u')
    except Exception as e:
        await message.answer(text='Произошла ошибка, обратитесь к разработчику)', reply_markup=anon_kb)
        logger.exception(e)
        await state.finish()
        await AnonStates.anon.set()
    else:
        # await message.answer(text='Идет процесс регистрации...\nДля завершения нажми на котика)',
        #                     reply_markup=cat_kb)

        await message.answer(text='Все отлично! Теперь вы зарегестрированы.', reply_markup=stud_kb())
        logger.info(f'New user: '
                    f'name - {0} surname - {1} group - {2}'.format(log_encode(data['name']),
                                                                   log_encode(data['surname']),
                                                                   log_encode(data['group_id'])))
        await state.finish()
        await StudentStates.student.set()


'''
# FINAL REGISTRATION
@dp.message_handler(state=RegistrationStates.final)
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Все отлично! Теперь вы зарегестрированы.', reply_markup=stud_kb())
    data = await state.get_data()
    logger.info(f'New user: '
                f'name - {0} surname - {1} group - {2}'.format(log_encode(data['name']),
                                                               log_encode(data['surname']),
                                                               log_encode(data['group_id'])))
    await state.finish()
    await StudentStates.student.set()
'''


# USER DON'T AGREE WITH INTRODUCED DATA
@dp.message_handler(Text(equals='нет', ignore_case=True), state=RegistrationStates.insert_sql)
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Пройдите регистрацию заново!', reply_markup=anon_kb)
    await state.finish()
    await AnonStates.anon.set()

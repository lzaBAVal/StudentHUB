import aiogram.utils.markdown as md

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from bot import keyboard as kb
from bot.states.states import AnonStates, RegistrationStates, StudentStates

from functions.find_group import group_search

from loader import dp, db, bot
from logs.logging_core import init_logger, log_encode

logger = init_logger()


@dp.message_handler(lambda message: message.text.lower() == "отмена", state=RegistrationStates)
async def reg_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await AnonStates.anon.set()
    await message.answer('Регистрация отменена', reply_markup=kb.anon_kb)


@dp.message_handler(state=RegistrationStates.name)
async def reg_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(text='Введите вашу фамилию', reply_markup=kb.register_kb)
    await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.surname)
async def reg_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await message.answer(text='Введите наименование вашей группы. Вы должны ввести строку вида \'сиб 19 6\'')
    await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.find_group)
async def search_group(message: types.Message):
    result = await group_search(message.text)
    logger.info('Client is finding himself group - ', log_encode(message.text))
    if result == -1:
        await message.answer(
            text='Не могу разобрать что вы пишите, попробуйте снова. Напомню, наименование группы должно быть такого '
                 'формата - "cиб 19 6"')
    else:
        comp_match, match, other_match = result
        if comp_match:
            kboard = kb.createButtons(comp_match)
            await message.answer(text='Это наименование вашей группы?', reply_markup=kboard)
            await RegistrationStates.next()
        elif match:
            kboard = kb.createButtons(match)
            await message.answer(text='Не найдено точное наименование вашей группы. Ваша группа есть в этом списке?',
                                 reply_markup=kboard)
            # await RegistrationStates.next()
        elif other_match:
            kboard = kb.createButtons(other_match)
            await message.answer(
                text='Я не нашел ничего похожего. Посмотрите список групп который я вам предоставил. Возможно там '
                     'будет то что вам нужно',
                reply_markup=kboard)
            # await RegistrationStates.next()
        else:
            await message.answer(
                text='Вашей группы у меня нет. Если вы уверены что верно вводите название группы, напишите об этом '
                     'разработчику, он вам поможет',
                reply_markup=kb.anon_kb)
            await AnonStates.anon.set()


@dp.message_handler(state=RegistrationStates.accept_all_data)
async def accept_all_data(message: types.Message, state: FSMContext):
    try:
        group_id = await db.get_group_id(message.text)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('ERROR: произошла ошибка. Регистрация отменена')
        await state.finish()
        await AnonStates.anon.set()
    else:
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
        logger.exception(e)
        await state.finish()
        await AnonStates.anon.set()
    else:
        await message.answer(text='Идет процесс регистрации...\nДля завершения нажми на котика)',
                             reply_markup=kb.cat_kb)
        await RegistrationStates.next()


@dp.message_handler(state=RegistrationStates.final)
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Все отлично! Теперь вы зарегестрированы.', reply_markup=kb.stud_kb)
    data = await state.get_data()
    logger.info(f'New user: '
                f'name - {0} surname - {1} group - {2}'.format(log_encode(data['name']),
                                                               log_encode(data['surname']),
                                                               log_encode(data['group_id'])))
    await state.finish()
    await StudentStates.student.set()


@dp.message_handler(state=RegistrationStates.insert_sql, text='Нет')
async def reg_final(message: types.Message, state: FSMContext):
    await message.answer(text='Пройдите регистрацию заново!', reply_markup=kb.anon_kb)
    await state.finish()
    await AnonStates.anon.set()

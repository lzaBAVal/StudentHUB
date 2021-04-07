import bot.keyboard as kb

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from bot.states.states import AdminCheckUser, AdminGiveRights, AdminTakeAwayRights
from functions.admin.admin_func import get_list_of_users, output_bio
from loader import dp, db
from config import myid
from bot.handlers.handlers import def_user


@dp.message_handler(IDFilter(myid), commands=['help_admin'], state='*')
async def check_user(message: types.Message):
    await message.answer(
        '/cancel_func - отменяет текущий процесс операции\n'
        '/id - выведет ваш chat_id который вам выдал телеграм\n'
        '/bio - выведет информацию о вас: имя, фамилия, группа, дата регистрации, ваш статус\n'
        '/group_info - выведет информацию о вашей группе, имя старосты, количество человек в состоящих в группе и '
        'пользующихся ботом\n '
        '/check_user_bio - показывает информацию о пользователе чей id вы введет\n'
        '/users_list - выводит список студентов с их именем, группой, id\n'
        '/give_rights - выдать права старосты студенту\n'
        '/take_away_rights - забрать права старосты у студента\n')


@dp.message_handler(IDFilter(myid), commands=['cancel_func'], text=['Отмена'], state='*')
async def cancel_func(message: types.Message):
    await message.answer('Вы отменили операцию')
    await def_user(message)


@dp.message_handler(IDFilter(myid), commands=['users_list'], state='*')
async def users_list(message: types.Message):
    response = await get_list_of_users(db, message.chat.id)
    await message.answer(response)


@dp.message_handler(IDFilter(myid), commands=['check_user_bio'], state='*')
async def check_user_bio(message: types.Message):
    await message.answer('Введите id студента, о котором вы хотите получить информацию')
    await AdminCheckUser.user_id.set()


@dp.message_handler(IDFilter(myid), state=AdminCheckUser.user_id)
async def check_user_get_list(message: types.Message):
    msg = message.text
    if msg.isdigit():
        resp = dict((await db.admin_get_user_bio(message.chat.id, int(msg)))[0])
        resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True)
        await message.answer(resp)
    else:
        await message.answer('Введите id пользователя!')


@dp.message_handler(IDFilter(myid), commands=['give_rights'], state='*')
async def give_rights(message: types.Message):
    await message.answer('Введите id человека, которому вы хотите выдать привилегии старосты')
    await AdminGiveRights.user_id.set()


@dp.message_handler(IDFilter(myid), state=AdminGiveRights.user_id)
async def give_rights_data(message: types.Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        resp = dict((await db.admin_get_user_bio(message.chat.id, int(msg)))[0])
        print(resp)
        resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
        async with state.proxy() as data:
            data['user'] = msg
        await message.answer(resp + str('\nВыдать права данному пользователю?'), reply_markup=kb.question_kb)
        await AdminGiveRights.next()
    else:
        await message.answer('Введите id пользователя!')


@dp.message_handler(lambda message: message.text.lower() == "да", IDFilter(myid), state=AdminGiveRights.issue)
async def give_rights(message: types.Message, state: FSMContext):
    user = int((await state.get_data())['user'])
    print(user)
    await db.update_privilege(1, user)
    resp = dict((await db.admin_get_user_bio(message.chat.id, user))[0])
    resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
    await message.answer(resp + '\nПрава выданы!', reply_markup=kb.stud_kb)
    await def_user(message)


@dp.message_handler(lambda message: message.text.lower() == "нет", IDFilter(myid), state=AdminGiveRights.issue)
async def give_rights(message: types.Message, state: FSMContext):
    await state.finish()
    await def_user(message)


@dp.message_handler(IDFilter(myid), commands=['take_away_rights'], state='*')
async def give_rights(message: types.Message):
    await message.answer('Введите id человека, у которого вы хотите забрать привилегии старосты')
    await AdminCheckUser.user_id.set()


@dp.message_handler(IDFilter(myid), state=AdminTakeAwayRights.user_id)
async def give_rights_data(message: types.Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        resp = dict((await db.admin_get_user_bio(message.chat.id, int(msg)))[0])
        resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
        async with state.proxy() as data:
            data['user'] = msg
        await message.answer(resp + str('\nЗабрать права у данного пользователя??'), reply_markup=kb.question_kb)
        await AdminGiveRights.next()
    else:
        await message.answer('Введите id пользователя!')


@dp.message_handler(lambda message: message.text.lower() == "да", IDFilter(myid), state=AdminTakeAwayRights.issue)
async def give_rights(message: types.Message, state: FSMContext):
    user = state.get_data('user')
    await db.update_privilege(0, user)
    resp = dict((await db.admin_get_user_bio(message.chat.id, user))[0])
    resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
    await message.answer(resp + '\nПрава забраны!')
    await def_user(message)


@dp.message_handler(lambda message: message.text.lower() == "нет", IDFilter(myid), state=AdminTakeAwayRights.issue)
async def give_rights(message: types.Message, state: FSMContext):
    await state.finish()
    await def_user(message)


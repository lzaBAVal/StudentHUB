from bot.keyboard.keyboard import get_delete_message_button, question_kb
from bot.strings.messages import help_admin_str
from schedule_json.harvest.harvest_main import harvest_groups, harvest_arhit_sched
from utils.log.logging_core import init_logger

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from bot.handlers.InitialHandler import def_user
from bot.states.states import AdminCheckUser, AdminGiveRights, AdminTakeAwayRights, AdminPrintArhit, AdminBanUser, \
    AdminUnbanUser
from old_config import myid
from functions.admin.admin_func import get_list_of_users, output_bio, create_hash
from loader import db
from misc import dp
from utils.log.output import get_last_logs, get_last_critical_logs
from schedule_json.output.get_schedule_object import check_raw_sched

logger = init_logger()

'''
@dp.message_handler(commands=['harvest'], state='*')
async def harvest(message: types.Message):
    await harvest_arhit_sched(db)
    await message.answer('Test')
'''


# CANCEL FUNCTION
@dp.message_handler(IDFilter(myid),
                    commands=['cancel_func'],
                    state='*')
async def cancel_func(message: types.Message, state: FSMContext):
    await message.answer('Вы отменили операцию')
    await def_user(message, state)


# TODO harvest groups
# HARVEST GROUPS
@dp.message_handler(IDFilter(myid),
                    commands=['harvest_groups'],
                    state='*')
async def cancel_func(message: types.Message, state: FSMContext):
    await message.answer('Вы начали обновление групп университета')
    await harvest_groups()


@dp.message_handler(IDFilter(myid),
                    commands=['harvest_arhit_sched'],
                    state='*')
async def cancel_func(message: types.Message, state: FSMContext):
    await message.answer('Вы начали обновление расписания групп университета')
    await harvest_arhit_sched()


# GET HELP FOR ADMIN
@dp.message_handler(IDFilter(myid),
                    commands=['helpadmin'],
                    state='*')
async def helpadmin(message: types.Message):
    await message.answer(help_admin_str, reply_markup=get_delete_message_button())


# GET LAST CRITICAL LOGS
@dp.message_handler(IDFilter(myid),
                    commands=['last_critical'],
                    state='*')
async def get_last_critical_logs(message: types.Message):
    await message.answer(get_last_critical_logs(), reply_markup=get_delete_message_button())


# GET LAST LOGS
@dp.message_handler(IDFilter(myid),
                    commands=['last_logs'],
                    state='*')
async def check_user(message: types.Message):
    result = get_last_logs()
    await message.answer(result, reply_markup=get_delete_message_button())


# GET SCHEDULE OF GROUP OR ARHIT 1
@dp.message_handler(IDFilter(myid),
                    commands=['print_arhit', 'print_group'],
                    state='*')
async def print_arhit(message: types.Message, state: FSMContext):
    await message.answer('Введите id группы чье расписание вы хотите увидеть')
    type_sched = message.text
    if type_sched == '/print_arhit':
        type_sched = 'sched_arhit'
    elif type_sched == '/print_group':
        type_sched = 'sched_group'
    else:
        await message.answer('Error')
        return 0
    await state.set_data({'type': type_sched})
    await AdminPrintArhit.select.set()


# GET SCHEDULE OF GROUP OR ARHIT 2
@dp.message_handler(IDFilter(myid), state=AdminPrintArhit.select)
async def print_arhit(message: types.Message, state: FSMContext):
    if message.text.isdecimal():
        group_id = int(message.text)
        type_sched = await state.get_data()
        res = await check_raw_sched(group_id, type_sched['type'])
        await message.answer(res, reply_markup=get_delete_message_button())
    else:
        await message.answer('Некорректное id группы')
    await cancel_func(message, state)


# GET LIST OF USERS
@dp.message_handler(IDFilter(myid), commands=['users_list'], state='*')
async def users_list(message: types.Message):
    response = await get_list_of_users(db, message.chat.id)
    await message.answer(response, reply_markup=get_delete_message_button())


# ADD NEW HASH
@dp.message_handler(IDFilter(myid), commands=['add_hash'], state='*')
async def new_hash(message: types.Message):
    try:
        hash = await create_hash(db, message)
    except Exception as exc:
        logger.exception(exc)
        await message.answer('Не удалось добавить хэш')
    else:
        await message.answer(hash)


# GET FREE HASCHES
@dp.message_handler(IDFilter(myid), commands=['get_free_hashes'], state='*')
async def get_free_hashes(message: types.Message):
    hashes = (await db.get_free_hashes())
    result = ''
    for key in hashes:
        result += key['key_md5'] + '\n'
    if result == '':
        result = 'Свободных хешей нет, создайте новые'
    await message.answer(result)


# BAN USER 1
# TODO ban user
@dp.message_handler(IDFilter(myid), commands=['ban'], state='*')
async def ban_user(message: types.Message):
    await message.answer('Введите id студента, которого вы хотите забанить')
    await AdminBanUser.user_id.set()


# BAN USER 2
@dp.message_handler(IDFilter(myid), state=AdminBanUser.user_id)
async def ban_user_select(message: types.Message, state: FSMContext):
    msg = message.text
    print(msg)
    print(type(msg))
    if msg.isdigit():
        try:
            resp = await db.admin_get_user_bio(message.chat.id, int(msg))
            resp = dict(resp[0])
        except Exception as exc:
            logger.exception(exc)
            await cancel_func(message)
        else:
            resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True)
            await db.update_ban(message.chat.id, int(msg), True)
            await message.answer(f'{resp}\nBan set - 1')
            await dp.current_state(chat=msg, user=msg).finish()
            await def_user(message, state)
    else:
        await message.answer('Введите id пользователя!')


# UNBAN USER 1
# TODO unban user
@dp.message_handler(IDFilter(myid), commands=['unban'], state='*')
async def unban_user(message: types.Message):
    await message.answer('Введите id студента, которого вы хотите разбанить')
    await AdminUnbanUser.user_id.set()


# UNBAN USER 2
@dp.message_handler(IDFilter(myid), state=AdminUnbanUser.user_id)
async def unban_user_select(message: types.Message, state: FSMContext):
    msg = message.text
    print(msg)
    print(type(msg))
    if msg.isdigit():
        try:
            msg = int(msg)
            resp = await db.admin_get_user_bio(message.chat.id, msg)
            resp = dict(resp[0])
        except Exception as exc:
            logger.exception(exc)
            await cancel_func(message)
        else:
            resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True)
            await db.update_ban(message.chat.id, msg, False)
            await message.answer(f'{resp}\nBan set - 0')
            await dp.current_state(chat=msg, user=msg).finish()
            await def_user(message, state)
    else:
        await message.answer('Введите id пользователя!')


# CHECK INFO ABOUT USER 1
@dp.message_handler(IDFilter(myid), commands=['check_user_bio'], state='*')
async def check_user_bio(message: types.Message):
    await message.answer('Введите id студента, о котором вы хотите получить информацию')
    await AdminCheckUser.user_id.set()


# CHECK INFO ABOUT USER 2
@dp.message_handler(IDFilter(myid), state=AdminCheckUser.user_id)
async def check_user_get_list(message: types.Message):
    msg = message.text
    if msg.isdigit():
        try:
            resp = dict((await db.admin_get_user_bio(message.chat.id, int(msg)))[0])
        except Exception as exc:
            logger.exception(exc)
            await cancel_func(message)
        else:
            resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True)
            await message.answer(resp)
    else:
        await message.answer('Введите id пользователя!')


# GIVE RIGHTS TO USER 1
@dp.message_handler(IDFilter(myid), commands=['give_rights'], state='*')
async def give_rights(message: types.Message):
    await message.answer('Введите id человека, которому вы хотите выдать привилегии старосты')
    await AdminGiveRights.user_id.set()


# GIVE RIGHTS TO USER 2
@dp.message_handler(IDFilter(myid), state=AdminGiveRights.user_id)
async def give_rights_data(message: types.Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        try:
            resp = dict((await db.admin_get_user_bio(message.chat.id, int(msg)))[0])
        except Exception as exc:
            logger.exception(exc)
            await cancel_func(message)
        else:
            resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
            async with state.proxy() as data:
                data['user'] = msg
            await message.answer(resp + str('\nВыдать права данному пользователю?'), reply_markup=question_kb)
            await AdminGiveRights.next()
    else:
        await message.answer('Введите id пользователя!')


# GIVE RIGHTS TO USER 3 YES
@dp.message_handler(lambda message: message.text.lower() == "да", IDFilter(myid), state=AdminGiveRights.issue)
async def give_rights_yes(message: types.Message, state: FSMContext):
    user = int((await state.get_data())['user'])
    await db.update_privilege(1, user)
    resp = dict((await db.admin_get_user_bio(message.chat.id, user))[0])
    resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
    await message.answer(resp + '\nПрава выданы!')
    await def_user(message, state)


# GIVE RIGHTS TO USER 3 NO
@dp.message_handler(lambda message: message.text.lower() == "нет", IDFilter(myid), state=AdminGiveRights.issue)
async def give_rights_no(message: types.Message, state: FSMContext):
    await def_user(message, state)


# TAKE AWAY RIGHTS 1
@dp.message_handler(IDFilter(myid), commands=['take_away_rights'], state='*')
async def take_away_rights(message: types.Message):
    await message.answer('Введите id человека, у которого вы хотите забрать привилегии старосты')
    await AdminTakeAwayRights.user_id.set()


# GIVE RIGHTS TO USER 2
@dp.message_handler(IDFilter(myid), state=AdminTakeAwayRights.user_id)
async def give_rights_data(message: types.Message, state: FSMContext):
    msg = message.text
    if msg.isdigit():
        try:
            resp = dict((await db.admin_get_user_bio(message.chat.id, int(msg)))[0])
        except Exception as exc:
            logger.exception(exc)
            await cancel_func(message)
        else:
            resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
            async with state.proxy() as data:
                data['user'] = msg
            await message.answer(resp + str('\nЗабрать права у данного пользователя??'), reply_markup=question_kb)
            await AdminTakeAwayRights.next()
    else:
        await message.answer('Введите id пользователя!')


# GIVE RIGHTS TO USER 3 YES
@dp.message_handler(lambda message: message.text.lower() == "да", IDFilter(myid), state=AdminTakeAwayRights.issue)
async def give_rights(message: types.Message, state: FSMContext):
    user = int((await state.get_data('user'))['user'])
    await db.update_privilege(0, user)
    resp = dict((await db.admin_get_user_bio(message.chat.id, user))[0])
    resp = output_bio(resp, id_chat=True, name=True, surname=True, group=True, privilege=True)
    await message.answer(resp + '\nПрава забраны!')
    await def_user(message)


# GIVE RIGHTS TO USER 3 NO
@dp.message_handler(lambda message: message.text.lower() == "нет", IDFilter(myid), state=AdminTakeAwayRights.issue)
async def give_rights(message: types.Message, state: FSMContext):
    await def_user(message, state)

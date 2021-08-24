import hashlib
from datetime import datetime

from DB import db_query
from log.logging_core import init_logger

logger = init_logger()


async def get_list_of_users():
    result = ''
    response = await db_query.admin_get_users_list()
    for user in response:
        result += str(output_bio(dict(user), chat_id=True, name=True, surname=True, group=True, privilege=True)) + '\n'
    return result


def output_bio(user: dict, chat_id=False, name=False, surname=False, group=False, privilege=False, ban=False):
    result = ''
    print(user)
    if chat_id:
        result += f'id = {user["chat_id"]} |'
    if name:
        result += f'name = {user["name"]} | '
    if surname:
        result += f'surname = {user["surname"]} | '
    if group:
        result += f'group = {user["group_id"]} | '
    if privilege:
        result += f'privilege = {user["privilege"]} | '
    if ban:
        result += f'ban = {user["ban"]} | '
    result += '\n'
    return result


async def create_hash(message):
    hash = hashlib.md5(bytes(str((datetime.now())).encode('utf-16'))).hexdigest()
    # await db_query.add_key(hash, datetime.now().strftime("%d-%m-%Y %H:%M"))
    await db_query.add_key(hash, datetime.now())
    logger.debug(f'User - {message.chat.id}. New hash has been added')
    return hash

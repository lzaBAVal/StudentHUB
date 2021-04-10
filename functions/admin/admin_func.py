import hashlib
from datetime import datetime
from logs.scripts.logging_core import init_logger

logger = init_logger()


async def get_list_of_users(db, chat_id):
    result = ''
    response = await db.admin_get_users_list(chat_id)
    for user in response:
        result += str(output_bio(dict(user), id_chat=True, name=True, surname=True, group=True, privilege=True)) + '\n'
    return result


def output_bio(user: dict, id_chat=False, name=False, surname=False, group=False, privilege=False):
    result = ''
    if id_chat:
        result += f'id = {user["id_chat"]} |'
    if name:
        result += f'name = {user["u_name"]} | '
    if surname:
        result += f'surname = {user["surname"]} | '
    if group:
        result += f'group = {user["group_id"]} | '
    if privilege:
        result += f'privilege = {user["privilege"]} | '
    result += '\n'
    return result


async def create_hash(db, message):
    hash = hashlib.md5(bytes(str((datetime.now())).encode('utf-16'))).hexdigest()
    await db.add_key(hash, datetime.now().strftime("%d-%m-%Y %H:%M"))
    logger.debug(f'User - {message.chat.id}. New hash has been added')
    return hash

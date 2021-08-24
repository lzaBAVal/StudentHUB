from DB import db_query
from DB.models import Student


async def get_list_of_classmates(chat_id):
    result = ''
    users = await db_query.admin_get_users_classmates(chat_id)
    for user in users:
        result = output_bio(user, chat_id=False, name=True, surname=True, group=False)
    return result


def output_bio(user: dict, chat_id=False, name=False, surname=False, group=False):
    result = ''
    if chat_id:
        result += f'ID = {user["chat_id"]} |'
    if name:
        result += f'Имя = {user["name"]} | '
    if surname:
        result += f'Фамилия = {user["surname"]} | '
    if group:
        result += f'Группа = {user["group_id"]} | '
    result += '\n'
    return result


async def get_bio(chat_id):
    response = await Student.filter(chat_id=chat_id).all().values('chat_id', 'name', 'surname', 'group_id')
    response = response[0]
    return output_bio(response, chat_id=True, name=True, surname=True, group=True)

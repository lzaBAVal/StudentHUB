async def get_list_of_classmates(db, chat_id):
    result = ''
    responce = await db.admin_get_users_classmates(chat_id)
    for user in responce:
        result = output_bio(dict(user), id_chat=False, name=True, surname=True, group=False)
    return result


def output_bio(user: dict, id_chat=False, name=False, surname=False, group=False):
    result = ''
    if id_chat:
        result += f'ID = {user["id_chat"]} |'
    if name:
        result += f'Имя = {user["u_name"]} | '
    if surname:
        result += f'Фамилия = {user["surname"]} | '
    if group:
        result += f'Группа = {user["group_id"]} | '
    result += '\n'
    return result


async def get_bio(db, chat_id):
    response = (await db.get_user(chat_id))[0]
    return output_bio(response, id_chat=True, name=True, surname=True, group=True)

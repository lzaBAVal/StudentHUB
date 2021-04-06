
async def get_list_of_users(db, chat_id):
    result = ''
    responce = await db.admin_get_users_list(chat_id)
    for user in responce:
        result = output_bio(dict(user), id_chat=True, name=True, surname=True, group=True, privilege=True)
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

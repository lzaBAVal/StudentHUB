from models import Student


async def get_list_of_classmates(db, chat_id):
    result = ''
    responce = await db.admin_get_users_classmates(chat_id)
    group_id = await Student.filter(id_chat=chat_id).values_list('group_id')
    group_id = group_id[0][0]
    users = await Student.filter(group_id=group_id).all().values('chat_id', 'u_name', 's_name', 'group_id')
    users_dict = users[0]
    print(users_dict)
    # sql_query = "select chat_id, u_name, surname, group_id from student where group_id = (select group_id from " \
    #                     "student where chat_id = $1) "
    for user in responce:
        result = output_bio(users_dict, id_chat=False, name=True, surname=True, group=False)
    return result


def output_bio(user: dict, id_chat=False, name=False, surname=False, group=False):
    result = ''
    if id_chat:
        result += f'ID = {user["chat_id"]} |'
    if name:
        result += f'Имя = {user["u_name"]} | '
    if surname:
        result += f'Фамилия = {user["s_name"]} | '
    if group:
        result += f'Группа = {user["group_id"]} | '
    result += '\n'
    return result


async def get_bio(chat_id):
    response = await Student.filter(id_chat=chat_id).all().values('chat_id', 'u_name', 's_name', 'group_id')
    response = response[0]
    return output_bio(response, id_chat=True, name=True, surname=True, group=True)

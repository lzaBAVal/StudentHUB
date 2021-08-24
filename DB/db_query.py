from DB.models import Student, Key


async def update_privilege(privilege: int, chat_id: int):
    await Student.filter(chat_id=chat_id).update(privilege=privilege)


"""
async def update_privilege(self, privilege: int, chat_id: int) -> str:
    sql_query = "update student set privilege = $1 where chat_id = $2"
    logger.info(f'Student - {id_chat} update_privilege, privilege - {privilege}')
    return await self.pool.execute(sql_query, privilege, id_chat)
"""


async def admin_get_user_bio(chat_id: int) -> dict:
    user = await Student.filter(chat_id=chat_id).values('chat_id', 'name', 'surname', 'group_id', 'privilege')
    return user[0]


"""
async def admin_get_user_bio(self, admin_id_chat: int, id_chat: int) -> str:
    sql_query = "select chat_id, u_name, surname, group_id, privilege, ban from student where chat_id = $1"
    logger.info(f'Student - {id_chat} admin_get_user. Checks {admin_id_chat}')
    return await self.pool.fetch(sql_query, id_chat)
"""


async def admin_get_users_list():
    users = await Student.all().values('chat_id', 'name', 'surname', 'group_id', 'privilege')
    return users


"""
async def admin_get_users_list(self, admin_id_chat: int) -> str:
    sql_query = "select chat_id, u_name, surname, group_id, privilege from student"
    logger.info(f'admin_get_users_list. Checks {admin_id_chat}')
    return await self.pool.fetch(sql_query)
"""


async def get_free_hashes():
    keys = await Key.filter(chat_id=None).values('key_md5')
    return keys


"""
    async def get_free_hashes(self):
        return await self.pool.fetch('select key_md5 from keys where chat_id is null')
"""


async def add_key(hash: str, date):
    await Key.create(key_md5=hash, time_created=date)


"""
    async def add_key(self, hash: str, date: str):
        sql_query = 'insert into keys(key_md5, time_created) values ($1, $2)'
        return await self.pool.execute(sql_query, hash, date)
"""


async def admin_get_users_classmates(chat_id):
    group_id = await Student.filter(chat_id=chat_id).values_list('group_id')
    group_id = group_id[0][0]
    users = await Student.filter(group_id=group_id).all().values('chat_id', 'name', 'surname', 'group_id')
    return users

"""
async def admin_get_users_classmates(self, id_chat: int) -> str:
    sql_query = "select chat_id, u_name, surname, group_id from student where group_id = (select group_id from " \
                "student where chat_id = $1) "
    logger.info(f'admin_get_users_classmates. Checks {id_chat}')
    return await self.pool.fetch(sql_query, id_chat)
"""


async def get_group_name_user(chat_id: int):
    group_id = await Student.filter(chat_id=chat_id).values('group_id')
    return group_id[0]


"""
async def get_group_name_user(self, id_inc: int) -> str:
    sql_query = "select group_name from student where chat_id = $1"
    return await self.pool.fetch(sql_query, id_inc)
"""


# See the group_id (group_name in database)
async def update_captain(chat_id, hash, date, group_id):
    await Key.filter(key_md5=hash).update(chat_id=chat_id, time_start_use=date)

"""
async def update_captain(self, id_chat: str, hash: str, date: str, group_name: str):
    sql_query = 'update keys set (chat_id, time_start_use, group_name) = ($1, $3, $4) where key_md5 = $2;'
    logger.info(f'Student - {id_chat} update_captain')
    return await self.pool.execute(sql_query, id_chat, hash, date, group_name)
"""
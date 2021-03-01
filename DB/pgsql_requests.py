def add_user(chat_id: int, name: str, surname: str, group_id: int, privilege: int) -> str:
    result = "insert into student (id_chat, u_name, surname, group_id, privilege) values ({0}, \'{1}\', \'{2}\', {3}, b\'{4}\')".format(chat_id, name, surname, group_id, privilege)
    return result

def get_user(chat_id: int, name: str, surname: str, group_id: int, privilege: int) -> str:
    result = "select * from student where id_chat={0}".format(chat_id)
    return result

def get_group_sched(id_chat: int):
    result = 'select sched_dict from sched_stud where group_id=(select group_id from student where id_chat={0})'.format(id_chat)
    return result

def get_group_name(id_inc: int) -> str:
    result = "select group_name from groups_students where id_inc={0}".format(id_inc)
    return result

def get_institution(id_inc: int):
    result = 'select sched from institution where id_inc = {0}'.format(id_inc)
    return result

def get_institution_url_groups(id_inc: int):
    result = 'select url_for_groups from institution where id_inc = {0}'.format(id_inc)
    return result

def get_groups_values(institution_id: int):
    result = 'select group_url_value, id_inc from groups_students where institution_id = {0}'.format(institution_id)
    return result

def get_institution_ids():
    result = 'select id_inc from institution'
    return result

def update_privilege(privilege: int, chat_id: int) -> str:
    result = "update student set privilege = b\'{0}\' where id_chat = {1}".format(privilege, chat_id)
    return result

def insert_schedule(group_id, sched_dict):
    result = "insert into sched_stud(group_id, sched_dict) values ({0}, \'{1}\');".format(group_id, sched_dict)
    return result

def insert_group(group_name: str, id: int, url_value: str):
    result = 'insert into groups_students(group_name, institution_id, group_url_value) values (\'{0}\', {1}, \'{2}\');'.format(group_name, id, url_value)
    return result

def insert_institution(instit_name: str, url: str, url_for_groups: str):
    result = 'insert into institution(instit_name, sched, url_for_groups) values (\'{0}\', \'{1}\', \'{2}\');'.format(instit_name, url, url_for_groups)
    return result

def test_connect():
    result = 'select version();'
    return result
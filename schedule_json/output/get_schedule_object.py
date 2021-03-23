import base64

from schedule_json.output import type_of_sched
from loader import db

async def get_sched_type(id_chat: int, type_of_shed: int):
    sched = await get_sched(id_chat)
    if type_of_shed == 1:
        return type_of_sched.all_schedule(sched)
    elif type_of_shed == 2:
        return type_of_sched.schedule_for_today(sched)
    elif type_of_shed == 3:
        return type_of_sched.current_lesson(sched)
    elif type_of_shed == 4:
        return type_of_sched.schedule_for_tommorow(sched)
    else:
        print('get_sched_type WTF!!!')
        return -1


async def get_sched(id_chat: int):
    sched = await db.get_group_sched(id_chat=id_chat)
    if dict(sched)['sched_group'] is None:
        sched = str(dict(await db.get_arh_sched(id_chat))['sched_arhit'])
        await db.update_group_sched(sched, id_chat)
        sched = dict(await db.get_group_sched(id_chat=id_chat))
    sched = dict(sched)['sched_group']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
    return sched


'''
    sched = dict(await db.get_group_sched(id_chat=id_chat))
    if sched['sched_group'] is None:
        sched = await db.get_arh_sched(id_chat=id_chat)
        sched = dict(sched)['sched_arhit']
    else:
        sched = dict(sched)['sched_group']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
'''
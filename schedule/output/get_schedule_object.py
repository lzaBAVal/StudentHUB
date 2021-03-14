import base64

from schedule.output import type_of_sched
from loader import db

async def get_sched(id_chat: int, type_of_shed: int):
    sched = await db.get_group_sched(id_chat=id_chat)
    sched = dict(sched)['sched_dict']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
    if type_of_shed == 1:
        return type_of_sched.all_schedule(sched)
    elif type_of_shed == 2:
        return type_of_sched.schedule_for_today(sched)
    elif type_of_shed == 3:
        return type_of_sched.current_lesson(sched)
    else:
        print('get_sched WTF!!!')
        return -1


async def get_sched_list(id_chat: int):
    sched = await db.get_group_sched(id_chat=id_chat)
    sched = dict(sched)['sched_dict']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
    return sched
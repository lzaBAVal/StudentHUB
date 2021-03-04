import asyncio
import base64

from schedule_parce import parcing
from loader import db

async def get_sched(id_chat: int, type_of_shed: int):
    sched = await db.get_group_sched(id_chat=id_chat)
    sched = dict(sched)['sched_dict']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
    if type_of_shed == 1:
        return parcing.all_schedule(sched)
    elif type_of_shed == 2:
        return parcing.schedule_for_today(sched)
    elif type_of_shed == 3:
        return parcing.current_lesson(sched)
    else:
        print('get_sched WTF!!!')
        return -1

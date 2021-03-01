import asyncio
import base64

from schedule_parce import parcing
from DB.pgsql_conn import pgsql_conn
from DB.pgsql_requests import get_group_sched

def get_sched(id_chat: int, type_of_shed: int):
    sched = list(dict(asyncio.get_event_loop().run_until_complete(pgsql_conn(get_group_sched(id_chat)))[0]).values())[0]
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))

    if type_of_shed == 1:
        return parcing.all_shedule(sched)
    elif type_of_shed == 2:
        return parcing.schedule_for_today(sched)
    elif type_of_shed == 3:
        return parcing.current_lesson(sched)
    else:
        print('get_sched WTF!!!')
        return -1


print(get_sched(690976128, 1))
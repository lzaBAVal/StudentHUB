import asyncio
import base64

from DB.pgsql import pgsql_conn, async_get_loop
from DB.pgsql_requests import get_institution, get_institution_ids, insert_group,\
    get_institution_url_groups, get_groups_values, insert_schedule
from harvest.harvest_groups import search_group
from harvest.harvest_schedules import search_schedule

def get_ids():
    instit_ids = asyncio.get_event_loop().run_until_complete(pgsql_conn(request=get_institution_ids()))
    ids = []
    for i in instit_ids:
        ids.append(dict(i)['id_inc'])
    return ids


def harvest_groups():
    instit_ids = get_ids()

    for i in instit_ids:
        instit_url = dict(asyncio.get_event_loop().run_until_complete(pgsql_conn(get_institution(int(i))))[0])['sched']
        groups = search_group(instit_url)
        req_list = []
        for group in groups:
            req_list.append(insert_group(group, i, groups[group]))
        asyncio.get_event_loop().run_until_complete(pgsql_conn(request_l=req_list))


def harvest_schedule(id: int = None):
    if id:
        instit_ids = [id]
    else:
        instit_ids = get_ids()

    for i in instit_ids:
        url_group = str(list(dict(asyncio.get_event_loop().run_until_complete(pgsql_conn(request=get_institution_url_groups(i)))[0]).values())[0])
        groups_values = asyncio.get_event_loop().run_until_complete(pgsql_conn(request=get_groups_values(i)))
        for i in groups_values:
            print(list(i))
            url = str(url_group.replace('{value}', list(i)[0]))
            sched = str(search_schedule(url))
            sched64 = str(base64.b64encode(sched.encode('utf-8')))[2:-1]
            asyncio.get_event_loop().run_until_complete(pgsql_conn(insert_schedule(list(i)[1], sched64)))


harvest_schedule(5)
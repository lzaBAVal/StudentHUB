import asyncio
import base64
from datetime import datetime

import aioschedule

from logs.scripts.logging_core import init_logger
from schedule_json.harvest.harvest_groups import search_group
from schedule_json.harvest.harvest_schedules import search_schedule
from schedule_json.output.get_schedule_object import update_sched, get_sched

logger = init_logger()


class Harvest:
    def __init__(self, db):
        self.t = datetime.now().timestamp()
        self.db = db

    async def update(self):
        return await get_ids(self.db)

    async def check_time(self, t):
        if self.t - datetime.timestamp() > 60:
            await Harvest.update(self)
        else:
            await asyncio.sleep(70)


async def get_ids(db):
    instit_ids = await db.get_institution_ids()
    ids = []
    for i in instit_ids:
        ids.append(dict(i)['id_inc'])
    return ids


'''
async def harvest_groups(db):
    from schedule.harvest.harvest_groups import search_group
    instit_ids = await get_ids()

    for i in instit_ids:
        instit_url = dict(db.get_institution(int(i)))['sched']
        groups = search_group(instit_url)
        for group in groups:
            await db.add_group(group, i, groups[group])

async def harvest_schedule(db, id: int = None):
    if id:
        instit_ids = [id]
    else:
        instit_ids = await get_ids()

    for i in instit_ids:
        url_group = str(list(dict(db.get_institution_url_groups(i))[0].values())[0])
        groups_values = await db.get_groups_values(i)
        for i in groups_values:
            print(list(i))
            url = str(url_group.replace('{value}', list(i)[0]))
            sched = str(search_schedule(url))
            sched64 = str(base64.b64encode(sched.encode('utf-8')))[2:-1]
            await db.insert_schedule((list(i)[1], sched64))
'''


async def harvest_groups(db):
    instit_ids = await get_ids(db)

    for instit_id in instit_ids:
        instit_url = dict(list(await db.get_institution(int(instit_id)))[0])['url']
        groups = search_group(instit_url)
        exist_groups = await db.get_all_groups()
        for name in exist_groups:
            if list(name)[0] in groups:
                groups.pop(str(list(name)[0]))
        if groups == {}:
            logger.debug('No changes in harvest of the groups of the institution - (id) ' + str(instit_id))
        else:
            for group in groups:
                logger.debug('New groups - ' +
                             str(group.encode('utf-8')) + ' ' +
                             str(str(instit_id).encode('utf-8')) + ' ' +
                             str(groups[group].encode('utf-8')))
                await db.add_group(group, instit_id, groups[group])
    logger.debug('Harvest groups has been ended')


async def harvest_arhit_sched(db):
    instit_ids = await get_ids(db)

    for i in instit_ids:
        print('Institution: ' + str(i))
        url_group = str(dict(list(await db.get_institution_url_groups(i))[0])['url_for_groups'])
        groups_values = await db.get_groups_values(i)
        
        for j in groups_values:
            group_url_value: str = str(list(j)[0])
            id_inc: int = int(list(j)[1])
            try:
                url = str(url_group.replace('{value}', group_url_value))
                sched = str(search_schedule(url))
                sched
                if sched == -1:
                    continue
                sched64 = str(base64.b64encode(sched.encode('utf-8')), 'utf-8')
                exist_sched = dict(list(await db.get_groups_sched_name_arhit(id_inc))[0])['sched_arhit']
                if hash(sched64) != hash(exist_sched):
                    logger.debug(f'Changed the schedule id = {id_inc}')
                    await db.update_arhit_sched(sched64, id_inc)
            except Exception as exc:
                logger.warn('Institution id - ' + str(i) + ', group_value: ' + group_url_value)
                logger.exception(exc)
    logger.debug('Harvest schedule has been ended')


async def fix_schedule(id_chat, sched_type):
    sched = await get_sched(id_chat, 'sched_arhit')
    await update_sched(id_chat, sched, sched_type)


'''
async def harvest_group_sched(db):
    instit_ids = await get_ids(db)

    for i in instit_ids:
        url_group = str(dict(list(await db.get_institution_url_groups(i))[0])['url_for_groups'])
        groups_values = await db.get_groups_values(i)
        for j in groups_values:
            url = str(url_group.replace('{value}', list(j)[0]))
            sched = str(search_schedule(url))
            sched64 = str(base64.b64encode(sched.encode('utf-8')))[2:-1]
            exist_sched = dict(list(await db.get_groups_sched_name_group(list(j)[1]))[0])
            if sched64 == exist_sched['sched_group'] or exist_sched['sched_group'] == None:
                logger.debug('Changed the schedule - id = ' + str(str(list(j)[1]).encode('utf-8')))
                await db.update_group_sched(str(sched64), list(j)[1])
    logger.debug('Harvest schedule has been ended')
'''


async def scheduler(db):
    # aioschedule.every(12).hours.do(harvest_groups, db)
    aioschedule.every(4).hours.do(harvest_arhit_sched, db)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

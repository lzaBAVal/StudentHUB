import asyncio
import base64
from datetime import datetime

import aioschedule

from models import Group
from models.institution import Institution
from utils.log.logging_core import init_logger
from schedule_json.harvest.harvest_groups import search_group
from schedule_json.harvest.harvest_schedules import search_schedule
from schedule_json.output.get_schedule_object import update_sched, get_sched

logger = init_logger()


class Harvest:
    def __init__(self, db):
        self.t = datetime.now().timestamp()
        self.db = db

    async def update(self):
        return await get_ids()

    async def check_time(self, t):
        if self.t - datetime.timestamp() > 60:
            await Harvest.update(self)
        else:
            await asyncio.sleep(70)


async def get_ids():
    instit_ids = await Institution.all().values_list('id')
    ids = []
    print(f"instit_ids - {instit_ids} - harvest_main")
    for i in instit_ids:
        ids.append(i[0])
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


async def harvest_groups():
    instit_ids = await get_ids()

    for instit_id in instit_ids:
        institution_url = await Institution.filter(id=instit_id).values_list('url')
        institution_url = institution_url[0][0]
        groups = search_group(institution_url)
        exist_groups = await Group.all().values_list('group_name')

        # Are there new groups in DB
        for name in exist_groups:
            if list(name)[0] in groups:
                groups.pop(str(list(name)[0]))
        if groups is None:
            logger.debug('No changes in harvest of the groups of the institution - (id) ' + str(instit_id))
        else:
            for group in groups:
                logger.debug(f"New group - "
                             f"{str(group.encode('utf-8'))}"
                             f"{str(str(instit_id).encode('utf-8'))}"
                             f"{str(groups[group].encode('utf-8'))}")
                await Group(group_name=group, institution_id=instit_id, group_url_value=groups[group]).save()
    logger.debug('Harvest groups has been ended')


async def harvest_arhit_sched():
    instit_ids = await get_ids()

    for institution_id in instit_ids:
        logger.debug(f'Institution: {institution_id}')
        url_group = await Institution.filter(id=institution_id).values_list('url_for_groups')
        url_group = url_group[0][0]
        groups_values = await Group.filter(institution_id=institution_id).values_list('group_url_value', 'id')

        for j in groups_values:
            group_url_value: str = str(list(j)[0])
            group_id: int = int(list(j)[1])
            try:
                url = str(url_group.replace('{value}', group_url_value))
                sched = str(search_schedule(url))

                if sched == -1:
                    continue
                sched64 = str(base64.b64encode(sched.encode('utf-8')), 'utf-8')
                exist_sched = await Group.filter(id=group_id).values_list('group_name', 'sched_arhit')
                exist_sched = exist_sched[0][1]
                if hash(sched64) != hash(exist_sched):
                    logger.debug(f'Changed the schedule id = {group_id}')
                    await Group.filter(id=group_id).update(sched_arhit=sched64)
            except Exception as exc:
                logger.warn(f"Institution id - {institution_id}, group_value: {group_url_value}")
                logger.exception(exc)
    logger.debug('Harvest schedule has been ended')


async def fix_schedule(chat_id, sched_type):
    sched = await get_sched(chat_id, 'sched_arhit')
    await update_sched(chat_id, sched, sched_type)


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

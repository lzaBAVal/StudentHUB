import base64
import loader

from schedule_json.output import type_of_sched
from logs.scripts.logging_core import init_logger
from vars import Sched

logger = init_logger()


async def get_sched_type(id_chat: int, type_of_shed: int, whose_sched: str) -> [int, str]:
    sched = await get_sched(id_chat, whose_sched)
    if sched == -1:
        return 'Ошибка в коде'
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


async def get_sched(id_chat: int, sched_type: str) -> [dict, int]:
    if sched_type == 'sched_group':
        sched = await loader.db.get_group_sched(id_chat)
    elif sched_type == 'sched_arhit':
        sched = await loader.db.get_arhit_sched(id_chat)
    elif sched_type == 'sched_user':
        sched = await loader.db.get_user_sched(id_chat)
    else:
        return -1
    sched = dict(sched)[sched_type]
    print(sched_type)
    #if sched == 'LTE=':
    #    await update_sched(id_chat, dict(await loader.db.get_arhit_sched(id_chat))['sched_arhit'], sched_type)
    if sched is not None:
        sched = decode_normalise_sched(sched)
        if sched == -1:
            return -1
        return sched
    else:
        sched_raw = dict(await loader.db.get_arhit_sched(id_chat))['sched_arhit']
        sched = decode_normalise_sched(sched_raw)
        if sched == -1:
            return -1
        await update_sched(id_chat, sched, sched_type)
        logger.info(f'User - {0}, has created personal schedule {1}'.format(id_chat, sched_type))
        return sched


async def update_sched(id_chat: int, sched: dict, sched_type: str):
    sched = encode_normalise_sched(sched)
    if sched_type == 'sched_group':
        await loader.db.update_group_sched(sched, id_chat)
    elif sched_type == 'sched_arhit':
        await loader.db.update_arhit_sched(sched, id_chat)
    elif sched_type == 'sched_user':
        await loader.db.update_user_sched(sched, id_chat)
    else:
        return -1

    logger.info(f'User - {0} update_{1}'.format(id_chat, sched_type))


def check_sched(sched: dict) -> bool:
    try:
        Sched.parse_obj(sched)
    except Exception as exp:
        logger.warn('The schedule does not meet the standard')
        logger.exception(exp)
        return False
    else:
        return True


def decode_sched(sched: str) -> dict:
    try:
        return eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
    except Exception as exc:
        logger.warn('Can\'t decode schedule - ')
        logger.exception(exc)


def encode_sched(sched: dict) -> str:
    try:
        return str(base64.b64encode(str(sched).encode('utf-8')), 'utf-8')
    except Exception as exc:
        logger.warn('Can\'t encode schedule - ' + str(sched))
        logger.exception(exc)


def decode_normalise_sched(sched: str):
    sched: dict = decode_sched(sched)
    if check_sched(sched) == False:
        logger.warn('The schedule does not meet the standard')
        return -1
    else:
        return sched


def encode_normalise_sched(sched: dict):
    if check_sched(sched) == False:
        logger.warn('The schedule does not meet the standard')
        return -1
    else:
        return encode_sched(sched)


'''
    sched = dict(await db.get_group_sched(id_chat=id_chat))
    if sched['sched_group'] is None:
        sched = await db.get_arhit_sched(id_chat=id_chat)
        sched = dict(sched)['sched_arhit']
    else:
        sched = dict(sched)['sched_group']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
'''

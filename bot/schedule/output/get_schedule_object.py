import base64

from DB.models import Student, Group
from bot.schedule.output import type_of_sched
from bot.vars import Sched
from log.logging_core import init_logger

logger = init_logger()


async def get_sched_type(chat_id: int, type_of_shed: int, whose_sched: str) -> [int, str]:
    sched = await get_sched(chat_id, whose_sched)
    sched_parts = await Student.filter(chat_id=chat_id).values_list('sched_parts')
    sched_parts = sched_parts[0][0]
    parts = parse_sched_parts(sched_parts)
    if sched == -1:
        return 'Ошибка в коде'
    if type_of_shed == 1:
        return type_of_sched.all_schedule(sched, **parts)
    elif type_of_shed == 2:
        return type_of_sched.schedule_for_today(sched, **parts)
    elif type_of_shed == 3:
        return type_of_sched.current_lesson(sched, **parts)
    elif type_of_shed == 4:
        return type_of_sched.schedule_for_tommorow(sched, **parts)
    else:
        print('get_sched_type WTF!!!')
        return -1


async def get_sched(chat_id: int, sched_type: str) -> [dict, int]:
    print(f'sched_type: {sched_type}')
    if sched_type == 'sched_group' or sched_type == 'g':
        sched = await Student.filter(chat_id=chat_id).select_related('group').all()
        sched = sched[0].group.sched_group
    elif sched_type == 'sched_arhit':
        sched = await Student.filter(chat_id=chat_id).select_related('group').all()
        sched = sched[0].group.sched_arhit
    elif sched_type == 'sched_user' or sched_type == 'p':
        sched = await Student.filter(chat_id=chat_id).values_list('sched_user')
        sched = sched[0][0]
    else:
        return -1
    if isinstance(sched, str):
        sched = decode_normalise_sched(sched)
        if isinstance(sched, int):
            return -1
        return sched
    elif sched is None:
        logger.info(f'User - {chat_id}. Empty schedule')
        related_query = await Student.filter(chat_id=chat_id).select_related('group').all()
        sched_raw = related_query[0].group.sched_arhit
        sched = decode_normalise_sched(sched_raw)
        if isinstance(sched, int):
            return -1
        elif isinstance(sched, dict):
            await update_sched(chat_id, sched, sched_type)
            logger.info(f'User - {chat_id}, has created {sched_type}')
            return sched
        else:
            return -1
    else:
        return -1


async def check_raw_sched(group_id: int, sched_type: str):
    if sched_type == 'sched_group':
        _sched = await Group.filter(id=group_id).values_list('sched_group')
        _sched = _sched[0][0]
    elif sched_type == 'sched_arhit':
        _sched = await Group.filter(id=group_id).values_list('sched_arhit')
        _sched = _sched[0][0]
    else:
        return -1
    _sched = dict(_sched)[sched_type]
    sched = decode_normalise_sched(_sched)
    if isinstance(sched, dict):
        return str(sched) + '\nPOSITIVE. Валидная структурв'
    logger.warn(f'Broken schedule: {group_id}')
    sched = decode_sched(_sched)
    return str(sched) + '\nNEGATIVE. Проверка на валидность структуры не пройдена'


async def update_sched(chat_id: int, sched: dict, sched_type: str):
    print(sched_type)
    sched = encode_normalise_sched(sched)
    if isinstance(sched, str):
        if sched_type == 'sched_group' or sched_type == 'g':
            id_inc = await Student.filter(chat_id=chat_id).values_list('group_id')
            id_inc = id_inc[0][0]
            await Group.filter(id=id_inc).update(sched_group=sched)
        elif sched_type == 'sched_arhit':
            id_inc = await Student.filter(chat_id=chat_id).values_list('group_id')
            id_inc = id_inc[0][0]
            await Group.filter(id=id_inc).update(sched_arhit=sched)
        elif sched_type == 'sched_user' or sched_type == 'p':  # p = personal
            await Student.filter(chat_id=chat_id).update(sched_user=sched)
        else:
            return -1
    else:
        return -1
    logger.info(f'User - {0} update_{1}'.format(chat_id, sched_type))


def parse_sched_parts(parts) -> dict:
    parts_dict = {
        'time': bool(int(parts[0])),
        'subgroup': bool(int(parts[1])),
        'lesson': bool(int(parts[2])),
        'teacher': bool(int(parts[3])),
        'classroom': bool(int(parts[4]))
    }
    return parts_dict


def compose_sched_parts(parts: dict) -> str:
    result = ''
    for i in parts:
        if parts[i]:
            result += '1'
        else:
            result += '0'
    return result


def check_sched(sched: dict) -> bool:
    try:
        Sched.parse_obj(sched)
    except Exception as exp:
        logger.warn('The schedule does not meet the standard')
        logger.exception(exp)
        return False
    else:
        return True


def decode_sched(sched: str, log=True) -> dict:
    try:
        return eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
    except Exception as exc:
        if log:
            logger.warn('Can\'t decode schedule - ')
            logger.exception(exc)
        return -1


def encode_sched(sched: dict) -> str:
    try:
        return str(base64.b64encode(str(sched).encode('utf-8')), 'utf-8')
    except Exception as exc:
        logger.warn('Can\'t encode schedule - ' + str(sched))
        logger.exception(exc)


def decode_normalise_sched(sched: str):
    sched: dict = decode_sched(sched)
    if sched == -1:
        logger.warn('The schedule is empty')
        return -1
    if not check_sched(sched):
        logger.warn('The schedule does not meet the standard')
        return -1
    else:
        return sched


def encode_normalise_sched(sched: dict):
    if not check_sched(sched):
        logger.warn('The schedule does not meet the standard')
        return -1
    else:
        return encode_sched(sched)


'''
    sched = dict(await db.get_group_sched(chat_id=chat_id))
    if sched['sched_group'] is None:
        sched = await db.get_arhit_sched(chat_id=chat_id)
        sched = dict(sched)['sched_arhit']
    else:
        sched = dict(sched)['sched_group']
    sched = eval(base64.b64decode(sched.encode('utf-8')).decode("utf-8"))
'''

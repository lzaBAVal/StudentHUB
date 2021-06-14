from models import Student
from utils.log.logging_core import init_logger

logger = init_logger()

personal = 'p'
general = 'g'
arhit = 'a'


async def whois(message) -> str:
    try:
        whose = (await Student.filter(chat_id=message.chat.id).values_list('whose_schedule'))
        whose = whose[0][0]
    except Exception as exc:
        logger.exception(exc)
        raise ValueError
    else:
        if whose == personal:            # personal
            whose = 'sched_user'
        elif whose == general:          # general
            whose = 'sched_group'
        elif whose == arhit:          # arhit
            whose = 'sched_arhit'
        else:
            raise ValueError
        return whose


def whois_str(whose):
    if whose == personal:
        whose = 'Личное расписание'
    elif whose == general:
        whose = 'Расписание группы'
    elif whose == arhit:
        whose = 'Расписание с https://aues.arhit.kz/'
    else:
        raise ValueError
    return whose


def whois_update(whose):
    if whose == personal:
        whose = 'Личное расписание'
    elif whose == general:
        whose = 'Расписание группы'
    elif whose == arhit:
        whose = 'Расписание с https://aues.arhit.kz/'
    else:
        raise ValueError
    return whose


from logs.scripts.logging_core import init_logger

logger = init_logger()


async def whois(db, message) -> str:
    try:
        whose = ((await db.get_whose_sched(message.chat.id))[0]['whose_schedule'])
    except Exception as exc:
        logger.exception(exc)
        raise ValueError
    else:
        if whose == 'personal':
            whose = 'sched_user'
        elif whose == 'general':
            whose = 'sched_group'
        elif whose == 'arhit':
            whose = 'sched_arhit'
        else:
            raise ValueError
        return whose


def whois_str(whose):
    if whose == 'personal':
        whose = 'Личное расписание'
    elif whose == 'general':
        whose = 'Расписание группы'
    elif whose == 'arhit':
        whose = 'Расписание с https://aues.arhit.kz/'
    else:
        raise ValueError
    return whose


def whois_update(whose):
    if whose == 'personal':
        whose = 'Личное расписание'
    elif whose == 'general':
        whose = 'Расписание группы'
    elif whose == 'arhit':
        whose = 'Расписание с https://aues.arhit.kz/'
    else:
        raise ValueError
    return whose


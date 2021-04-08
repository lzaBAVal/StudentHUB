from asyncio import sleep

from datetime import datetime

from logs.logging_core import init_logger

logger = init_logger()


async def add_captain(db, chat_id, hash):
    try:
        group_name = (await db.get_group_name_user(chat_id))[0]['group_name']
        print(group_name)
        await db.update_captain(chat_id, hash, datetime.now().strftime("%d-%m-%Y %H:%M"), group_name)
    except Exception as exc:
        logger.exception(exc)
        return -1
    else:
        await db.update_privilege(1, chat_id)

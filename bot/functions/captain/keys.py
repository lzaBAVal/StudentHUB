from datetime import datetime

from DB import db_query
from log.logging_core import init_logger

logger = init_logger()


async def add_captain(chat_id, hash):
    try:
        group_id = await db_query.get_group_name_user(chat_id)
        print(group_id)
        await db_query.update_captain(chat_id, hash, datetime.now(), group_id)
    except Exception as exc:
        logger.exception(exc)
        return -1
    else:
        await db_query.update_privilege('c', chat_id)

import hashlib

from datetime import datetime
from logs.logging_core import init_logger

logger = init_logger()


async def create_hashes(db):
    hash = hashlib.md5(bytes(str((datetime.now())).encode('utf-16'))).hexdigest()
    await db.add_key(hash)
    return hash


async def get_free_hashes(db):
    hashes = await db.get_free_hashes()
    return hashes


async def add_tester(db, chat_id, hash):
    await db.update_tester(chat_id, hash)

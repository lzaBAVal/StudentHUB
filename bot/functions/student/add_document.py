from hashlib import md5

from aiogram import types

from DB.models import Document
from utils.file_system import get_path


async def save_document(task, md_hash):
    await Document.filter(hash_file=md_hash).update(task_id=task)


async def keep_document(message: types.Message) -> str:
    print(f'message.document.file_id: {message.document.file_id}')
    file_id = message.document.file_id
    name_doc = str(file_id).encode('utf-8')
    hash = md5(name_doc).hexdigest()
    path = get_path(hash)
    await download_document(message, hash, path)
    await Document(hash_file=hash, telegram_id=file_id).save()
    return hash


async def download_document(message, hash, path):
    await message.document.download(f'{path}\\{hash}.jpg')


async def delete_document(message: types.Message):
    pass

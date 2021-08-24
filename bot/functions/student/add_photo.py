from hashlib import md5

from aiogram import types

from DB.models import Photo
from utils.file_system import get_path


async def save_photo(task, md_hash):
    await Photo.filter(hash_file=md_hash).update(task_id=task)


async def keep_photo(message: types.Message):
    # print(f'message.photo[-1].file_id: {message.photo[-1].file_id}')
    file_id = message.photo[-1].file_id
    name_photo = str(file_id).encode('utf-8')
    hash = md5(name_photo).hexdigest()
    path = get_path(hash)
    await download_photo(message, hash, path)
    await Photo(hash_file=hash, telegram_id=file_id).save()
    return hash


async def download_photo(message, hash, path):
    await message.photo[-1].download(f'{path}\\{hash}.jpg')


async def delete_photo(message: types.Message):
    pass

from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from models import Student


@dataclass
class CaptainFilter(BoundFilter):
    key = 'is_captain'

    def __init__(self, is_captain):
        self.is_captain = is_captain

    async def check(self, message: types.Message) -> bool:
        captain = await Student.filter(chat_id=message.chat.id).values_list('privilege')
        captain = captain[0]
        return captain


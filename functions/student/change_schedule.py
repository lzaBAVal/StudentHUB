from aiogram import types

from loader import db
from models import Student


async def check_privilege_whose(message: types.message, privilege):
    whose = (await Student.filter(id_chat=message.chat.id).values_list('whose_schedule'))
    whose = whose[0][0]
    if whose == 'general' and privilege == 1:
        return 0
    elif whose == 'personal':
        return 0
    else:
        await message.answer('Вы не староста и не можете менять расписание группы. Попросите у старосты права или '
                             'используйте персональное расписание.\n'
                             'Персональное расписание можно использовать по умолчанию, зайдя в '
                             '"Настройки аккаунта" -> "Тип расписания"')
        return 1

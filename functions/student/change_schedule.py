import bot.keyboard as kb

from aiogram import types

from loader import db


async def check_privilege_whose(message: types.message):
    whose = (await db.get_whose_sched(message.chat.id))[0]['whose_schedule']
    privilege = dict((await db.check_captain(message.chat.id))[0])['privilege']
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

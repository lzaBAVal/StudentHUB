from aiogram import types
from aiogram.dispatcher import FSMContext

from DB.models import Student


async def check_privilege_whose(message: types.message, state: FSMContext):
    whose = (await Student.filter(chat_id=message.chat.id).values_list('whose_schedule'))
    whose = whose[0][0]
    list_data: dict = (await state.get_data())
    print(list_data.get('captain_middleware'))
    print(f'whose: {whose}')
    if whose == 'g' and list_data.get('captain_middleware'):
        return 0
    elif whose == 'p':
        return 0
    else:
        await message.answer('Вы не староста и не можете менять расписание группы. Попросите у старосты права или '
                             'используйте персональное расписание.\n'
                             'Персональное расписание можно использовать по умолчанию, зайдя в '
                             '"Настройки аккаунта" -> "Тип расписания"')
        return 1

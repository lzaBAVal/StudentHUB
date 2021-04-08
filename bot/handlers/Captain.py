from aiogram import types

from bot.states.states import StudentStates, SetCaptainState
from bot import keyboard as kb
from functions.captain.keys import add_captain
from loader import dp, db


@dp.message_handler(state=SetCaptainState.set)
async def set_captain(message: types.Message):
    hash = message.text.strip()
    if len(hash) == 32:
        code = await add_captain(db, message.chat.id, hash, )
        if code == -1:
            await message.answer('Не удалось добавить ваш ключ, сообщите об этом старосте', reply_markup=kb.stud_kb)
        else:
            await message.answer('Отлично, теперь у вас есть права старосты.', reply_markup=kb.stud_kb)
        await StudentStates.student.set()

    else:
        await message.answer('Вы отправляете мне сомнительный ключ, проверьте правильно ли вы его вводите '
                             'или обратитесь к админам\nВы в главном меню', reply_markup=kb.stud_kb)
        await StudentStates.student.set()
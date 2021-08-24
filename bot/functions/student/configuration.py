from aiogram import types

import bot.keyboard.keyboard as kb


async def whose_schedule(message: types.message):
    await message.answer('', reply_markup=kb.configuration_kb)
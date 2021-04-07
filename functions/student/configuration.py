import bot.keyboard as kb

from aiogram import types


async def whose_schedule(message: types.message):
    await message.answer('', reply_markup=kb.configuration_kb)
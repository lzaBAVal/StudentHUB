from aiogram import types

from bot.keyboard.keyboard import delete_cb
from misc import dp


# DELETE MESSAGE
@dp.callback_query_handler(delete_cb.filter(action=['delete']), state='*')
async def cb_delete_message(query: types.CallbackQuery):
    await query.message.delete()

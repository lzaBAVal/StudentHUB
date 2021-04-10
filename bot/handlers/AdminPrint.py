from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter

from bot.handlers.Admin import cancel_func
from bot.states.states import AdminPrintArhit
from config import myid
from loader import dp
from schedule_json.output.get_schedule_object import check_raw_sched


@dp.message_handler(IDFilter(myid), state=AdminPrintArhit.select)
async def print_arhit(message: types.Message, state: FSMContext):
    if message.text.isdecimal():
        group_id = int(message.text)
        type_sched = await state.get_data()
        res = await check_raw_sched(group_id, type_sched['type'])
        await message.answer(res)
    else:
        await message.answer('Некорректное id группы')
    await cancel_func()

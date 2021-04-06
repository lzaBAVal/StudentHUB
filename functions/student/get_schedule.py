import bot.keyboard as kb

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.states.states import StudentStates
from schedule_json.change.change_sched import get_free_time
from schedule_json.output.get_schedule_object import get_sched_type, get_sched
from logs.logging_core import init_logger
from functions.whois import whois
from bot.strings.messages import *
from vars import WeekDays_RU

logger = init_logger()


async def get_all_schedule(message: types.Message, whose='personal'):
    try:
        whose = whois(whose)
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=1, whose_sched=whose)
    except Exception as exc:
        logger.exception(exc)
        await message.answer(cant_show_schedule_str)
    else:
        await message.answer(text=resp)


async def get_todays_shedule(message: types.Message, whose='personal'):
    try:
        whose = whois(whose)
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=2, whose_sched=whose)
        if isinstance(resp, tuple):
            await message.answer(resp[1])
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer(cant_show_schedule_str)
    else:
        await message.answer(text=resp)


async def get_next_lesson(message: types.Message, whose='personal'):
    try:
        whose = whois(whose)
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=3, whose_sched=whose)
        if isinstance(resp, tuple):
            await message.answer(resp[1])
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer(cant_show_schedule_str)
    else:
        await message.answer(text=resp)


async def get_tommorow_lesson(message: types.Message, whose='personal'):
    try:
        whose = whois(whose)
        resp = await get_sched_type(id_chat=message.chat.id, type_of_shed=4, whose_sched=whose)
        if isinstance(resp, tuple):
            await message.answer(resp[1])
            return 0
    except Exception as exc:
        logger.exception(exc)
        await message.answer(cant_show_schedule_str)
    else:
        await message.answer(text=resp)


async def get_output_free_time(message: types.message, whose='personal'):
    if message.text.lower() in WeekDays_RU:
        whose = whois(whose)
        sched = await get_sched(message.chat.id, whose)
        result = await get_free_time(message.text.lower(), sched)
        res = ''
        for i in range(len(result)):
            if i % 3 != 0:
                res += str(result[i]) + ' | '
            else:
                res += '\n| ' + str(result[i]) + ' | '
        await message.answer(str(res), reply_markup=kb.stud_kb)
        await StudentStates.student.set()
    else:
        await message.answer('Введите день недели!')

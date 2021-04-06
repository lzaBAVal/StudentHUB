import asyncio

from aiogram.dispatcher import FSMContext

import bot.keyboard as kb
import loader

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from bot.states.states import AnonStates, StudentStates, CaptainSchedule
from logs.logging_core import init_logger

logger = init_logger()


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator



class CheckStateMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = await loader.dp.current_state(user=message.from_user.id).get_state()
        if state is None:
            try:
                if not (await loader.db.check_user(message.chat.id)):
                    await AnonStates.anon.set()
                else:
                    await StudentStates.student.set()
            except Exception as exc:
                logger.exception(exc)
                await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)
        else:
            pass


class CheckCaptainMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        #state = loader.dp.current_state(user=message.from_user.id).get_state()
        if handler.__name__ == 'change_sched':
            try:
                captain = dict(await loader.db.check_captain(message.chat.id)[0])['privilege']
                if captain == 1:
                    await CaptainSchedule.select.set()
            except Exception as exc:
                logger.exception(exc)
                await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=.3, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param data:
        :param message:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed

        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 3:
            await message.reply('Не отправляйте сообщения слишком часто!')
            logger.warn('User - ' + str(message.chat.id) + ' send many messages')
        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')

import asyncio

import bot.keyboard.keyboard as kb
import misc

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from bot.states.states import AnonStates, StudentStates
from models import Student
from utils.log.logging_core import init_logger

logger = init_logger()


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class CheckBannedUser(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        data = await misc.dp.current_state(user=message.from_user.id).get_data()
        try:
            ban = data['ban_middleware']
        except Exception as exc:
            check = await Student.filter(id=message.chat.id).values_list('ban')
            if not (check == []):
                check = check[0]
                if not check:
                    check = 0
                else:
                    check = check[0]
                    # check = int(dict(check[0])['ban'])
                if check == 0:
                    await misc.dp.current_state(user=message.from_user.id).update_data({'ban_middleware': 0})
                    pass
                else:
                    await misc.dp.current_state(user=message.from_user.id).update_data({'ban_middleware': 1})
                    raise CancelHandler()
        else:
            if ban == 0:
                pass
            else:
                raise CancelHandler()


class CheckStateMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = await misc.dp.current_state(user=message.from_user.id).get_state()
        if state is None:
            try:
                user = await Student.filter(chat_id=message.chat.id).first()
                if not user:
                    print(f"user: {user}")
                    # if not (await loader.db.check_user(message.chat.id)):
                    await AnonStates.anon.set()
                else:
                    await StudentStates.student.set()
            except Exception as exc:
                logger.exception(exc)
                await message.answer(text='Что то пошло не так! Ошибка', reply_markup=kb.anon_kb)
        else:
            pass


class CheckCaptainMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        data = await misc.dp.current_state(user=message.from_user.id).get_data()
        try:
            captain = data['captain_middleware']
        except Exception:
            check = await Student.filter(chat_id=message.chat.id).values_list('privilege')
            if not (check == []):
                check = check[0]
                # sql_query = "select privilege from student where chat_id = $1"
                # check = await loader.db.check_captain(message.chat.id)
                if not check:
                    # user
                    check = 'u'
                else:
                    check = check[0]
                    # check = int(dict(check[0])['privilege'])
                if check == 'u':
                    await misc.dp.current_state(user=message.from_user.id).update_data({'captain_middleware': False})
                else:
                    await misc.dp.current_state(user=message.from_user.id).update_data({'captain_middleware': True})
        else:
            if not captain:
                await misc.dp.current_state(user=message.from_user.id).update_data({'captain_middleware': False})
            else:
                await misc.dp.current_state(user=message.from_user.id).update_data({'captain_middleware': True})


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

        print(handler.__name__)

        if handler.__name__ != 'upload_photo':
            try:
                await dispatcher.throttle(key, rate=limit)
            except Throttled as t:
                await self.message_throttled(message, t)
                raise CancelHandler()
        else:
            pass

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
            print(f"key true: {key}")
        else:
            key = f"{self.prefix}_message"
            print(f"key false: {key}")

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 3:
            await message.reply('Не отправляйте сообщения слишком часто!')
            logger.warn('Student - ' + str(message.chat.id) + ' send many messages')
        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')

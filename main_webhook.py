import loader
import ssl
from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web
from config import WEBHOOK_URL_PATH, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV, WEBAPP_HOST, WEBAPP_PORT
from logs.logging_core import init_logger

# ----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    bot = loader.bot
    dp = loader.dp
    logger = init_logger()

    from aiogram import executor
    from bot.handlers import dp

    logger.debug('Bot started')

    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    app.on_startup.append(loader.on_startup)
    app.on_shutdown.append(loader.on_shutdown)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)


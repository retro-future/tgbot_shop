from aiogram import executor

from tgbot.loader import dp
from tgbot.utils.db_api import db_gino
import filters, middlewares, handlers
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await db_gino.on_startup(dp)
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

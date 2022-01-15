from aiogram import executor
from bot.loader import dp
from bot.utils.db_api import db_gino
from bot.utils.set_bot_commands import set_default_commands
from bot.utils.notify_admins import on_startup_notify
from bot import middlewares, filters, handlers


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await db_gino.on_startup(dp)
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

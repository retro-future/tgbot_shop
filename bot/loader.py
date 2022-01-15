from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot.data import config
from bot.data.config import env

REDIS_HOST = env.str("redis_host")

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=REDIS_HOST)
dp = Dispatcher(bot, storage=storage)

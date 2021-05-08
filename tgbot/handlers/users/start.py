from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.update_data(liked_products=[])
    await message.answer(f"Привет, {message.from_user.full_name}!")

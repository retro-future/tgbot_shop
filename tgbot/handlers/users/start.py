from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from tgbot.keyboards.default.menu_kb import menu
from tgbot.loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.update_data(liked_products=[])
    await state.update_data(products={})
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer_animation(animation="CgACAgIAAxkDAAIaWGCeQ1YMN2DcOYRBAhg7uSxe0_qnAAJtDQAC0uPwSGmwRsty71onHwQ",
                                   caption=f"Привет, {message.from_user.full_name}!", reply_markup=menu)
    await message.answer_audio(audio="CQACAgIAAxkDAAIabGCeRRsjSVkcJK_r6k1IhS-r2aatAAJwDQAC0uPwSOHahvBFJIVmHwQ")

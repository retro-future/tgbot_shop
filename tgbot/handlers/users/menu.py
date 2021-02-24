import logging
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from tgbot.keyboards.default.menu_kb import menu
from tgbot.keyboards.inline.callback_datas import category_callback
from tgbot.keyboards.inline.category_kb import category_keyboard, subcategory_keyboard
from tgbot.loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Bosh Menyu:", reply_markup=menu)


@dp.message_handler(text="🛍 Tovarlar")
async def show_categories(message: types.Message):
    await message.answer("Вот что у нас есть", reply_markup=await category_keyboard())


@dp.callback_query_handler(category_callback.filter())
async def show_subcategory(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"callback_data={callback_data}")
    category_id = callback_data.get('category_id')
    await call.message.edit_reply_markup(reply_markup=await subcategory_keyboard(int(category_id)))

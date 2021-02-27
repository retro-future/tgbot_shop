import logging
from typing import Union

from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from tgbot.keyboards.default.menu_kb import menu
from tgbot.keyboards.inline.callback_datas import category_callback, multi_menu
from tgbot.keyboards.inline.category_kb import category_keyboard, subcategory_keyboard
from tgbot.loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Bosh Menyu:", reply_markup=menu)


@dp.message_handler(text="🛍 Tovarlar")
async def delegate_to_categories(message: types.Message):
    # await message.answer("Вот что у нас есть", reply_markup=await category_keyboard())
    await show_category(message)


async def show_category(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await category_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Смотри, что у нас есть", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def show_subcategory(call: CallbackQuery, category_id, **kwargs):  # category_id taking category_id
    markup = await subcategory_keyboard(int(category_id))                # from callback_data and give it
    logging.info(f"callback_id={category_id}")                           # keyboard generator
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(multi_menu.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    current_level = callback_data.get("level")
    category = callback_data.get("category_id")
    subcategory = callback_data.get("subcategory_id")
    item_id = callback_data.get("item_id")

    levels = {
        "0": show_category,
        "1": show_subcategory,
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        category_id=category,
        subcategory=subcategory,
        item_id=item_id
    )

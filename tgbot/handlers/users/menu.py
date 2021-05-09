import logging
from pprint import pprint
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery, InputFile
from tgbot.keyboards.default.menu_kb import menu
from tgbot.keyboards.inline.callback_datas import multi_menu
from tgbot.keyboards.inline.category_kb import category_keyboard, subcategory_keyboard
from tgbot.loader import dp, bot


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    # await message.answer("Главное Меню:")
    await message.reply(text="Главное Меню:", reply_markup=menu)


@dp.message_handler(text="🛍 Товары")
async def delegate_to_categories(message: types.Message, state: FSMContext):
    await show_category(message, state=state)


async def show_category(message: Union[types.Message, types.CallbackQuery], **kwargs):
    state_data = await kwargs['state'].get_data()
    if not state_data['liked_products']:
        markup = await category_keyboard()
    else:
        quantity = len(state_data['liked_products'])
        markup = await category_keyboard(has_liked_products=True, liked_products_quantity=quantity)
    if isinstance(message, types.Message):
        await message.answer("Смотри, что у нас есть", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        if call.inline_message_id:
            await bot.edit_message_text(text="Смотри что у нас есть", inline_message_id=call.inline_message_id)
            await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=markup)
        else:
            await call.message.edit_reply_markup(markup)


async def show_subcategory(call: CallbackQuery, category_id, **kwargs):
    logging.info(f"callback_id={category_id}")
    markup = await subcategory_keyboard(int(category_id))
    if call.inline_message_id:
        await bot.edit_message_text(text="Наши Товары", inline_message_id=call.inline_message_id)
        await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=markup)
    else:
        await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(multi_menu.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    current_level = callback_data.get("level")
    category = callback_data.get("category_id")
    subcategory = callback_data.get("subcategory_id")

    levels = {
        "0": show_category,
        "1": show_subcategory,
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        state=state,
        category_id=category,
        subcategory=subcategory,
    )


@dp.message_handler(Command("send_photo"))
async def send_photo(message: types.Message):
    photo_bytes = InputFile(path_or_bytesio="../products/2021/03/12/SamsungGalaxyS20Ultra__1_.jpeg")
    msg = await message.answer_photo(photo_bytes)
    file_id = msg.photo[-1].file_id
    print(len(file_id))


# @dp.message_handler(Command("show_product"))
# async def show_all_product(message: types.Message):
#     products_qs = await show_product()
#     for product in products_qs:
#         if not product.image_file_id:
#             photo_path = InputFile(path_or_bytesio="../" + product.image)
#             msg = await message.answer_photo(photo_path)
#             file_id = msg.photo[-1].file_id
#             await product.update(image_file_id=file_id).apply()
#         else:
#             photo_path = product.image_file_id
#             await message.answer_photo(photo_path)
#

# @dp.message_handler(Command("redis"))
# async def test_redis(message: types.Message):
#     user_id = message.from_user.id
#     data = {
#         1: "first value of dict, and yes Redis is Working"
#     }
#     await set_value(user=user_id, data=data)
#     await message.answer(text=await get_value(user_id))

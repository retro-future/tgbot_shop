from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.loader import dp


# @dp.inline_handler(text="")
# async def empty_query(query: types.InlineQuery):
#     await query.answer(
#         results=[
#             types.InlineQueryResultArticle(
#                 id="unknown",
#                 title="Введите какой-то запрос",
#                 input_message_content=types.InputTextMessageContent(
#                     message_text="Не обязательно жать при этом на кнопку",
#                     parse_mode="HTML"
#                 ),
#             ),
#         ],
#
#         cache_time=5)


# @dp.inline_handler()
# async def empty_query(query: types.InlineQuery):
#     word_list = ["cake", "beer"]
#     if query.query in word_list:
#         await query.answer(
#             results=[
#                 types.InlineQueryResultArticle(
#                     id="unknown",
#                     title=f"Написал {query.query}",
#                     input_message_content=types.InputTextMessageContent(
#                         message_text="Не обязательно жать при этом на кнопку",
#                         parse_mode="HTML"
#                     ),
#                 ),
#             ],
#
#             cache_time=5)
#     print(query.query)


@dp.message_handler(Command("show_apple"))
async def answer_to_message(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton("press button",
                                       switch_inline_query_current_chat="apples"))
    await message.answer("press the button", reply_markup=markup)
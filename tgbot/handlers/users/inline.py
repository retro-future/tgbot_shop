from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.loader import dp
from tgbot.filters import IsSubcategoryName
from tgbot.utils.db_api.quick_commands import show_products_inline


my_reply = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="не нажимай на меня ", callback_data="buy:5:apple")
    ]
])


@dp.inline_handler(IsSubcategoryName(), regexp="^.{4,}")
async def empty_query(query: types.InlineQuery):
    print(query.query)
    query_text = query.query
    products_qs = await show_products_inline(query_text)
    query_answer = []
    for product in products_qs:
        query_answer.append(
            types.InlineQueryResultArticle(
                id=str(product.id),
                title=product.title,
                input_message_content=types.InputTextMessageContent(
                    message_text=f"<a href='{product.image}'>{product.title}</a>", parse_mode="HTML"
                ),
                reply_markup=my_reply,
                description=str(product.price),
                thumb_url=product.image,
            )
        )
    await query.answer(
        results=query_answer,
        cache_time=20
    )
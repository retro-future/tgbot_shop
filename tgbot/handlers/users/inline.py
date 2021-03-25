from aiogram import types
from tgbot.keyboards.inline.product_kb import product_keyboard
from tgbot.loader import dp
from tgbot.filters import IsSubcategoryName
from tgbot.utils.db_api.quick_commands import show_products_inline


@dp.inline_handler(IsSubcategoryName(), regexp="^.{4,}")
async def empty_query(query: types.InlineQuery):
    query_text = query.query
    products_qs = await show_products_inline(query_text)
    query_answer = []
    for product in products_qs:
        subcategory_name = product.parent.tg_name
        category_id = product.parent.category_id
        markup = await product_keyboard(product.id, product.title, subcategory_name, product.price, category_id)
        query_answer.append(
            types.InlineQueryResultArticle(
                id=str(product.id),
                title=product.title,
                input_message_content=types.InputTextMessageContent(
                    message_text=f"<a href='{product.image}'>{product.title}</a>", parse_mode="HTML"
                ),
                reply_markup=markup,
                description=str(product.price),
                thumb_url=product.image,
            )
        )
    await query.answer(
        results=query_answer,
        cache_time=0
    )

from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot.loader import dp
from tgbot.filters import IsSubcategoryName
from tgbot.utils.db_api.quick_commands import show_products_inline, get_liked_product


@dp.inline_handler(IsSubcategoryName(), regexp="^.{4,}")
async def inline_products(query: types.InlineQuery, state: FSMContext):
    query_text = query.query
    query_answer, first_product = await show_products_inline(query_text, state)
    await query.answer(results=query_answer, cache_time=0)


@dp.inline_handler(text="💘 Избранное")
async def liked_list(query: types.InlineQuery, state: FSMContext):
    state_data = await state.get_data()
    liked_products_id = state_data['liked_products']
    query_answer = await get_liked_product(liked_products_id=liked_products_id, state=state)
    await query.answer(results=query_answer, cache_time=0)

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.loader import dp
from tgbot.utils.db_api.quick_commands import show_all_subcategory, get_product


class IsSubcategoryName(BoundFilter):

    async def check(self, query: types.InlineQuery) -> bool:
        subcategories_qs = await show_all_subcategory()
        subcategory_names = [subcategory.tg_name for subcategory in subcategories_qs]
        if query.query in subcategory_names:
            return True


# class UpdateStateInfo(BoundFilter):
#
#     async def check(self, call: types.CallbackQuery) -> bool:
#         product_id = call["data"].split(":")[1]
#
#         product = await get_product(int(product_id))
#         async with dp.current_state().proxy() as state_data:
#             state_data["product_info"].update({
#                 "product_id": product.id,
#                 "product_title": product.title,
#                 "product_price": float(product.price),
#                 "category_id": product.parent.category_id,
#                 "subcategory_name": product.parent.tg_name,
#             })
#         return True

# class CheckCart(BoundFilter):
#     async def check(self, call: types.CallbackQuery,  *args, **kwargs):
#         data = await dp.current_state().get_data()
#         if not data['products']:
#             await call.answer("Корзина Пуста")
#             return False
#
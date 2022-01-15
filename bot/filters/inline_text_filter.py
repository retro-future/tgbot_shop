from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.utils.db_api.quick_commands import show_all_subcategory


class IsSubcategoryName(BoundFilter):

    async def check(self, query: types.InlineQuery) -> bool:
        subcategories_qs = await show_all_subcategory()
        subcategory_names = [subcategory.tg_name for subcategory in subcategories_qs]
        if query.query in subcategory_names:
            return True

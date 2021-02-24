from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import category_callback, subcategory_callback
from tgbot.utils.db_api.quick_commands import get_parent_child, get_child_parent


async def category_keyboard():
    categories_qs = await get_parent_child()
    categories = InlineKeyboardMarkup(row_width=1)
    for category in categories_qs:
        categories.insert(InlineKeyboardButton(text=f"{category.name}",
                                               callback_data=category_callback.new(category_id=f"{category.id}")))
    return categories


async def subcategory_keyboard(category_id: int):
    subcategories_qs = await get_child_parent(category_id=category_id)
    subcategories = InlineKeyboardMarkup(row_width=1)
    for subcategory in subcategories_qs:
        subcategories.insert(InlineKeyboardButton(text=f"{subcategory.name}",
                                                  callback_data=
                                                  subcategory_callback.new(subcategory_id=f"{subcategory.id}")))
    return subcategories

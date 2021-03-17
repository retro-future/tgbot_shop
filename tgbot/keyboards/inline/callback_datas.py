from aiogram.utils.callback_data import CallbackData

multi_menu = CallbackData("navigate", "level", "category_id", "subcategory_id", "item_id")
category_callback = CallbackData("category", "level")
subcategory_callback = CallbackData("subcategory", "subcategory_id")


async def navigate_callback(level, category_id="0", subcategory_id="0", item_id="0"):
    return multi_menu.new(level=level, category_id=category_id, subcategory_id=subcategory_id, item_id=item_id)



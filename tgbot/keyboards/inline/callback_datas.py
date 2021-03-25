from aiogram.utils.callback_data import CallbackData

multi_menu = CallbackData("navigate", "level", "category_id", "subcategory_id", "item_id")
category_callback = CallbackData("category", "level")
subcategory_callback = CallbackData("subcategory", "subcategory_id")
buy_callback = CallbackData("buy", "product_id")


async def navigate_callback(level, category_id="0", subcategory_id="0", item_id="0"):
    return multi_menu.new(level=level, category_id=category_id, subcategory_id=subcategory_id, item_id=item_id)


async def product_callback(product_id: int):
    return buy_callback.new(product_id=product_id)

from aiogram.utils.callback_data import CallbackData

multi_menu = CallbackData("navigate", "level", "category_id", "subcategory_id", "item_id")
category_callback = CallbackData("category", "level")
subcategory_callback = CallbackData("subcategory", "subcategory_id")
buy_callback = CallbackData("buy", "product_id", "product_price", "edit", "reduce", "add", "category_id", "liked")
test_callback = CallbackData("test_callback", "number")
liked_product = CallbackData("liked_product", "add", "delete", "product_id")


def navigate_callback(level, category_id="0", subcategory_id="0", item_id="0"):
    return multi_menu.new(level=level, category_id=category_id, subcategory_id=subcategory_id, item_id=item_id)


def gen_buy_callback(product_id: str, product_price: int, edit: bool = False,
                     reduce: bool = False, add: bool = False, category_id: int = 0, liked: bool = False):
    return buy_callback.new(product_id=product_id, product_price=product_price, edit=edit,
                            reduce=reduce, add=add, category_id=category_id, liked=liked)

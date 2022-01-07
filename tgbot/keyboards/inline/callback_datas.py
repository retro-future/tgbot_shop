from aiogram.utils.callback_data import CallbackData

multi_menu = CallbackData("navigate", "level", "category_id", "subcategory_id", "item_id")
category_callback = CallbackData("category", "level")
subcategory_callback = CallbackData("subcategory", "subcategory_id")
buy_callback = CallbackData("buy", "product_id", "product_price", "category_id")
test_callback = CallbackData("test_callback", "number")
liked_product = CallbackData("liked_product", "product_id", "add", "delete")
edit_quantity = CallbackData("edit_product", "product_id", "edit", "reduce", "add")
pagination_callback = CallbackData("pagination", "page", "edit")
pagination_edit_callback = CallbackData("edit_pagination", "product_id", "edit", "add", "reduce", "page")
pagination_quantity_callback = CallbackData("pagination_quantity", "page")
user_address_callback = CallbackData("user_address", "id", "name")
shipping_callback = CallbackData("shipping", "name")
payment_callback = CallbackData("payment", "name")

# Callback data that contains "product_id" argument must be added here
CD_with_product_id = [
    buy_callback,
    liked_product,
    edit_quantity,
    pagination_edit_callback
]


def parse_callback(callback_data: str):
    parsed_callback = ""
    for callback in CD_with_product_id:
        try:
            parsed_callback = callback.parse(callback_data)
            break
        except ValueError:
            continue
    return parsed_callback


def navigate_callback(level, category_id="0", subcategory_id="0", item_id="0"):
    return multi_menu.new(level=level, category_id=category_id, subcategory_id=subcategory_id, item_id=item_id)


def gen_buy_callback(product_id: str, product_price: str = "0", category_id: int = 0):
    return buy_callback.new(product_id=product_id, product_price=product_price, category_id=category_id)


def gen_edit_callback(product_id: str, edit: bool = False, reduce: bool = False, add: bool = False):
    return edit_quantity.new(product_id=product_id, edit=edit, reduce=reduce, add=add)


def gen_pag_edit_call(product_id: str, page: int, edit: bool = False, reduce: bool = False, add: bool = False):
    return pagination_edit_callback.new(product_id=product_id, edit=edit, reduce=reduce, add=add, page=page)


def gen_pagination_callback(page: int = 1, edit: bool = False):
    return pagination_callback.new(page=page, edit=edit)

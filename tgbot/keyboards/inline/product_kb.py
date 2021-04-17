from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import navigate_callback, test_callback, gen_buy_callback


async def product_keyboard(product_id: str,
                           product_title: str,
                           tg_name: str,
                           product_price: int,
                           category_id: int) -> InlineKeyboardMarkup:
    current_level = 2
    markup = InlineKeyboardMarkup(row_width=2)
    callback_data = gen_buy_callback(product_id=product_id, product_price=product_price,
                                     category_id=category_id, edit=False)
    product_name = "Купить " + product_title + " " + str(product_price) + "$"
    markup.insert(InlineKeyboardButton(text=product_name, callback_data=callback_data))
    markup.add(InlineKeyboardButton(text="❤", callback_data=callback_data))
    markup.insert(InlineKeyboardButton(text="🛒", callback_data=callback_data))
    markup.add(InlineKeyboardButton(text="◀ Назад", callback_data=await navigate_callback(level=current_level - 1,
                                                                                          category_id=category_id)))
    markup.insert(InlineKeyboardButton(text="Еще " + tg_name, switch_inline_query_current_chat=tg_name))
    return markup


def product_edit_kb(data: dict, product_id: str) -> InlineKeyboardMarkup:
    product = data["products"][product_id]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="-1", callback_data=gen_buy_callback(product_id=product_id,
                                                                           product_price=product['price'],
                                                                           reduce=True, edit=True)),
            InlineKeyboardButton(text="✏" + str(product['quantity']) + "шт.",
                                 callback_data=gen_buy_callback(product_id=product_id,
                                                                product_price=product["price"],
                                                                edit=True)),
            InlineKeyboardButton(text="+1", callback_data=gen_buy_callback(product_id=product_id,
                                                                           product_price=product['price'],
                                                                           add=True, edit=True))
        ],
        [
            InlineKeyboardButton(text="❤", callback_data=test_callback.new(1)),
            InlineKeyboardButton(text="🛒 " + "$" + str(product["total"]), callback_data=test_callback.new(1))
        ],
        [
            InlineKeyboardButton(text="◀ Назад", callback_data=test_callback.new(1)),
            InlineKeyboardButton(text="Еще", callback_data=test_callback.new(1))
        ]
    ])
    return markup

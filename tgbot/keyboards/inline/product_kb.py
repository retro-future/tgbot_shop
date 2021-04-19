from decimal import Decimal

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import navigate_callback, test_callback, gen_buy_callback


async def product_keyboard(product_id: str, product_title: str, tg_name: str, product_price: int,
                           category_id: int, state: FSMContext) -> InlineKeyboardMarkup:
    current_level = 2
    markup = InlineKeyboardMarkup(row_width=2)
    callback_data = gen_buy_callback(product_id=product_id, product_price=product_price,
                                     category_id=category_id, edit=False)

    async with state.proxy() as state_data:
        try:
            quantity = state_data["products"][str(product_id)]["quantity"]
            product_name = f"{quantity} шт. | " + "Купить " + f'"{product_title}"' + "  " + str(product_price) + "$"
            total = str(total_func(state_data["products"]))
        except KeyError:
            product_name = "Купить " + f'"{product_title}"' + "  " + str(product_price) + "$"
            total = "0.00 $"
    markup.insert(InlineKeyboardButton(text=product_name, callback_data=callback_data))
    markup.add(InlineKeyboardButton(text="❤", callback_data=callback_data))
    markup.insert(InlineKeyboardButton(text="🛒" + total, callback_data=callback_data))
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
            InlineKeyboardButton(text="🛒 " + "$" + str(total_func(data["products"])), callback_data=test_callback.new(1))
        ],
        [
            InlineKeyboardButton(text="◀ Назад", callback_data=test_callback.new(1)),
            InlineKeyboardButton(text="Еще " + data["product_data"]["subcategory_name"],
                                 callback_data=test_callback.new(1))
        ]
    ])
    return markup


def total_func(product_list: dict):
    total = 0
    for key in product_list.keys():
        price = product_list[key]["price"]
        quantity = product_list[key]["quantity"]
        total += (Decimal(price) * quantity)
    return total
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import buy_callback, navigate_callback


async def product_keyboard(product_id: int, product_title: str, tg_name: str, product_price: int, category_id: int):
    current_level = 2
    markup = InlineKeyboardMarkup(row_width=2)
    callback_data = buy_callback.new(product_id=product_id)
    product_name = product_title + " " + str(product_price) + "$"
    markup.insert(InlineKeyboardButton(text=product_name, callback_data=callback_data))
    markup.add(InlineKeyboardButton(text="❤", callback_data=callback_data))
    markup.insert(InlineKeyboardButton(text="🛒", callback_data=callback_data))
    markup.add(InlineKeyboardButton(text="◀ Назад", callback_data=await navigate_callback(level=current_level - 1,
                                                                                          category_id=category_id)))
    markup.insert(InlineKeyboardButton(text="Еще " + tg_name, switch_inline_query_current_chat=tg_name))
    return markup

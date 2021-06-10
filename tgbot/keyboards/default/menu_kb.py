from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Товары"),
            KeyboardButton(text="🛒 Корзина"),
        ],
    ],
    resize_keyboard=True,
    selective=True)

import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.data.config import ADMINS
from tgbot.loader import bot
from tgbot.utils.cart_product_utils import create_cart_list


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def order_notify(state: FSMContext):
    async with state.proxy() as state_data:
        address = state_data["user_address"]
        phone_number = state_data['phone_number']
        order_number = state_data['order_number']
    cart_list = await create_cart_list(state)
    answer = f"Номер заказа: {order_number}\n\n{cart_list}\n\nАдрес доставки: {address}\n\nКонтакт: {phone_number}"
    for admin in ADMINS:
        try:
            await bot.send_message(admin, answer)
        except Exception as err:
            logging.exception(err)

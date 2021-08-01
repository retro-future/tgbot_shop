from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import LabeledPrice

from tgbot.data.config import PROVIDER_TOKEN
from tgbot.loader import dp, bot
from tgbot.utils.cart_product_utils import wipe_state_data
from tgbot.utils.db_api.quick_commands import get_product, update_order
from tgbot.utils.notify_admins import order_notify


@dp.message_handler(Command("invoices"))
async def show_invoices(message: types.Message):
    product = await get_product(1)
    await bot.send_invoice(chat_id=message.from_user.id,
                           title=product.title,
                           description=product.description,
                           provider_token=PROVIDER_TOKEN,
                           currency="UZS",
                           prices=[
                               LabeledPrice(
                                   label="Продукт",
                                   amount=3000_12
                               ),
                           ],
                           need_shipping_address=True,
                           payload="123456")


async def show_invoice(chat_id: str, state: FSMContext):
    async with state.proxy() as state_data:
        labeled_price_list = []
        product_list = state_data.get("products")
        product_count = len(product_list.keys())
        for key in product_list.keys():
            product = product_list[key]
            labeled_price_list.append(
                LabeledPrice(
                    label=f"{product['title']}\n{product['quantity']} шт. x ${product['price']}",
                    amount=int(product['total'].replace(".", ""))
                ))
        if state_data.get("courier"):
            labeled_price_list.append(LabeledPrice(label="Курьер", amount=5_00))
        await bot.send_invoice(chat_id=chat_id,
                               title=f"Заказ номер: {state_data.get('order_number')}",
                               description=f"Всего {product_count} продуктов",
                               provider_token=PROVIDER_TOKEN,
                               currency="USD",
                               prices=labeled_price_list,
                               payload="1234567")


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def payment_process(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    order_id = state_data.get("order_id")
    order_number = state_data.get("order_number")
    await update_order(order_id)
    answer = f"Спасибо, номер заказа {order_number}! Наш менеджер свяжется с вами для уточнения всех деталей."
    await message.answer(answer)
    await order_notify(state)
    await wipe_state_data(state, products=True)

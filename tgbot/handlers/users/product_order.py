from pprint import pprint
from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from decimal import Decimal

from tgbot.handlers.users.payments import show_invoice
from tgbot.keyboards.default.menu_kb import menu
from tgbot.keyboards.inline.callback_datas import user_address_callback, shipping_callback, payment_callback
from tgbot.keyboards.inline.order_keyboards import generate_addresses_keyboard, gen_check_keyboard, \
    gen_shipping_keyboard, gen_payment_keyboard
from tgbot.loader import dp, bot
from tgbot.states.order_states import OrderStates
from tgbot.utils.cart_product_utils import create_cart_list, gen_total_price, wipe_state_data
from tgbot.utils.db_api.quick_commands import get_user, get_ordered_products
from tgbot.utils.db_api.schemas.db_tables import OrdersGino, OrderProductGino, TgUserGino, UserAddresses
from tgbot.utils.generate_order_number import generate_order_number
from tgbot.utils.notify_admins import order_notify


async def create_order_db(state: FSMContext):
    state_data = await state.get_data()
    user_db_id = state_data.get("user_db_id")
    total_price = gen_total_price(state)
    order_number = generate_order_number()
    order = await OrdersGino.create(tg_user_id=user_db_id, order_number=order_number, total_price=total_price)
    await state.update_data(order_number=order_number)
    await state.update_data(order_id=order.id)


async def ordered_product_list(state: FSMContext):
    async with state.proxy() as state_data:
        order_id = state_data['order_id']
        for product_id in state_data['products'].keys():
            product = state_data['products'].get(product_id)
            await OrderProductGino.create(order_id=order_id, product_id=int(product_id),
                                          quantity=int(product['quantity']),
                                          single_price=Decimal(product['price']))


@dp.callback_query_handler(text="order")
async def create_order(call: types.CallbackQuery, state: FSMContext):
    user = await get_user(user_id=int(call.from_user.id))
    await state.update_data(user_db_id=user.id)
    markup = await generate_addresses_keyboard(state)
    await bot.send_message(call.from_user.id, text="Куда доставлять?",
                           reply_markup=markup)
    await OrderStates.Address.set()
    await call.answer()


@dp.callback_query_handler(user_address_callback.filter(), state=OrderStates.Address)
@dp.message_handler(state=OrderStates.Address)
async def accept_address(message: Union[types.Message, types.CallbackQuery], state: FSMContext, callback_data: dict = None):
    if isinstance(message, types.Message):
        chat_id = message.chat.id
        address = message.text
        state_data = await state.get_data()
        user_db_id = state_data.get("user_db_id")
        await UserAddresses.create(user_id=user_db_id, address=address)
        await state.update_data(user_address=address)
    elif isinstance(message, types.CallbackQuery):
        chat_id = message.from_user.id
        address = callback_data.get("name")
        await state.update_data(user_address=address)
        await state.reset_state(with_data=False)
        await message.answer()
    await bot.send_message(chat_id=chat_id, text="Чем Доставлять?", reply_markup=gen_shipping_keyboard())
    await OrderStates.Shipping.set()


@dp.message_handler(state=OrderStates.Shipping)
async def delegate_to_shipping_method(message: types.Message, state: FSMContext):
    await message.answer(text="Чем Доставлять?", reply_markup=gen_shipping_keyboard())


@dp.callback_query_handler(shipping_callback.filter(), state=OrderStates.Shipping)
async def shipping_method(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(shipping=callback_data.get("name"))
    await bot.send_message(call.message.chat.id, text='Как удобно оплатить?', reply_markup=gen_payment_keyboard())
    await OrderStates.Payment.set()
    await call.answer()


@dp.message_handler(state=OrderStates.Payment)
async def delegate_to_payment_method(message: types.Message, state: FSMContext):
    await message.answer(text='Как удобно оплатить?', reply_markup=gen_payment_keyboard())


@dp.callback_query_handler(payment_callback.filter(), state=OrderStates.Payment)
async def payment_method(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(payment=callback_data.get("name"))
    answer = "Почти готово! Поделитесь с нами вашим номером телефона, " \
             "чтобы мы могли связаться с вами. Или напишите его ниже в формате +998**9999999"
    await bot.send_message(call.message.chat.id, text=answer)
    await OrderStates.Phone_Number.set()
    await call.answer()


@dp.message_handler(state=OrderStates.Phone_Number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await is_correct(chat_id=message.chat.id, state=state)


async def is_correct(chat_id: str, **kwargs):
    state = kwargs['state']
    async with state.proxy() as state_data:
        address = state_data["user_address"]
        phone_number = state_data['phone_number']
        cart_list = await create_cart_list(state)
        answer = "Всё верно?\n\n" + f"{cart_list}\n<b>Адрес доставки</b>: <i>{address}</i>\n" \
                                    f"<b>Контакт</b>: <i>{phone_number}</i>"
    await bot.send_message(chat_id=chat_id, text=answer, reply_markup=gen_check_keyboard())
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text="make_order")
async def make_order(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    await create_order_db(state=state)
    await ordered_product_list(state=state)
    state_data = await state.get_data()
    if state_data.get("payment") == "card":
        await show_invoice(chat_id, state)
        await call.answer()
        return
    order_number = state_data.get("order_number")
    answer = f"Спасибо, номер заказа {order_number}! Наш менеджер свяжется с вами для уточнения всех деталей."
    await bot.send_message(chat_id=chat_id, text=answer)
    await order_notify(state)
    await wipe_state_data(state, products=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@dp.callback_query_handler(text="cancel_order")
async def cancel_order(call: types.CallbackQuery, state: FSMContext):
    await wipe_state_data(state)
    await bot.send_message(call.message.chat.id, text='Мы перебросили вас в главное меню, но ваша корзина на месте',
                           reply_markup=menu)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()

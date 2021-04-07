from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import buy_callback
from tgbot.keyboards.inline.product_kb import product_edit_kb
from tgbot.loader import dp, bot
from tgbot.states.cart_states import ProductStates
from tgbot.utils.cart_db import shopcart
from decimal import Decimal


@dp.callback_query_handler(buy_callback.filter(edit="False"))
async def add_to_cart(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    quantity = int(callback_data.get("quantity"))
    product_price = callback_data.get("product_price")
    product_id = callback_data.get("product_id")
    data = {
        "products": {
            str(product_id):
                {
                    "quantity": quantity,
                    "price": Decimal(product_price),
                    "total": quantity * Decimal(product_price)
                },
        },
    }
    markup = product_edit_kb(data, product_id)
    await shopcart.set_data(user=user_id, data=data)
    await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(buy_callback.filter(edit="True"), state=None)
async def edit_product_quantity(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    await bot.send_message(chat_id=user_id, text="Введите количество товара на которую хотите изменить")
    await ProductStates.QUANTITY_EDIT.set()


@dp.message_handler(state=ProductStates.QUANTITY_EDIT)
async def accept_product_quantity(message: types.Message, state: FSMContext):
    await message.answer(text=message.text)
    print(message)
    await message.answer("fuck you")
    await state.reset_state()

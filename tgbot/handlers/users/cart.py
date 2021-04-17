from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import buy_callback
from tgbot.keyboards.inline.product_kb import product_edit_kb
from tgbot.loader import dp, bot
from tgbot.states.cart_states import ProductStates
from decimal import Decimal


@dp.callback_query_handler(buy_callback.filter(edit="False", add="False", reduce="False"))
async def add_to_cart(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_price = callback_data.get("product_price")
    product_id = callback_data.get("product_id")
    total = 1 * Decimal(product_price)
    data = {
        "products": {
            product_id:
                {
                    "quantity": 1,
                    "price": product_price,
                    "total": float(total)
                },
        },
    }
    async with state.proxy() as state_data:
        if not state_data.get("products"):
            await state.update_data(data=data)
            await state.update_data(product_id=product_id)
        else:
            state_data["products"].update(data["products"])

    markup = product_edit_kb(data, product_id)
    await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(buy_callback.filter(edit="True", add="False", reduce="False"))
async def edit_product_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    this handler is for editing product quantity in Cart, so after clicking edit keyboard
    state for QuantityEdit will be set and may be finished only after sending a certain integer to the bot
    if not update product_id then quantity will be set for previous product
    :param call:
    :param callback_data:
    :param state:
    :return:
    """
    user_id = call.from_user.id
    await bot.send_message(chat_id=user_id, text="Введите количество товара на которую хотите изменить")
    await state.update_data(message_data=dict(call))
    await state.update_data(product_id=callback_data.get('product_id'))
    await ProductStates.QUANTITY_EDIT.set()


# @dp.message_handler(text="🛍 Товары", state=ProductStates.QUANTITY_EDIT)
# async def test_handler(message: types.Message):
#     print("im here")


@dp.message_handler(state=ProductStates.QUANTITY_EDIT)
async def accept_product_quantity(message: types.Message, state: FSMContext):
    """
    Here the QuantityEdit state will finish but data is going to be remain for further editing
    all variables below are used for making inline keyboards, as they need to provide information to callback_datas
    :param message:
    :param state:
    :return:
    """
    async with state.proxy() as state_data:
        quantity = int(message.text)
        inline_message_id = state_data.get("message_data")["inline_message_id"]
        products_list = state_data.get("products")
        product_price = products_list[state_data.get("product_id")]['price']
        products_list[state_data.get("product_id")]['quantity'] = quantity
        products_list[state_data.get("product_id")]['total'] = float(quantity * Decimal(product_price))

        await bot.edit_message_reply_markup(inline_message_id=inline_message_id,
                                            reply_markup=product_edit_kb(data=state_data,
                                                                         product_id=state_data.get('product_id')))
    await message.answer("fuck you")
    # pprint(await state.get_data())
    await state.reset_state(with_data=False)


@dp.callback_query_handler(buy_callback.filter(edit="True", add="True"))
@dp.callback_query_handler(buy_callback.filter(edit="True", reduce="True"))
async def plus_one_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as state_data:
        products_list = state_data.get("products")
        product_quantity = products_list[callback_data.get("product_id")]['quantity']
        if product_quantity == 0 and callback_data.get("reduce") == "True":
            return
        elif callback_data.get("reduce") == "True":
            products_list[callback_data.get("product_id")]['quantity'] -= 1
        elif callback_data.get("add") == "True":
            products_list[callback_data.get("product_id")]['quantity'] += 1

    await bot.edit_message_reply_markup(inline_message_id=call["inline_message_id"],
                                        reply_markup=product_edit_kb(data=state_data,
                                        product_id=callback_data.get("product_id")))
    pprint(await state.get_data())

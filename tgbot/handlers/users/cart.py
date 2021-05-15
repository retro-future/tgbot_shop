from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot.filters.inline_text_filter import UpdateStateInfo
from tgbot.keyboards.inline.callback_datas import buy_callback, liked_product, edit_quantity
from tgbot.keyboards.inline.gen_keyboard import director, builder
from tgbot.keyboards.inline.product_kb import product_edit_kb, product_keyboard
from tgbot.loader import dp, bot
from tgbot.states.cart_states import ProductStates
from decimal import Decimal


@dp.callback_query_handler(buy_callback.filter(), UpdateStateInfo())
async def add_to_cart(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_price = callback_data.get("product_price")
    product_id = callback_data.get("product_id")
    total = Decimal(product_price)
    products = {
        product_id:
            {
                "quantity": 1,
                "price": product_price,
                "total": float(total),
            },
    }
    async with state.proxy() as state_data:
        state_data["product_id"] = product_id
        if not state_data["products"]:
            state_data["products"] = products
        elif product_id not in state_data["products"].keys():
            state_data["products"].update(products)
        else:
            state_data["products"][product_id]["quantity"] += 1
            state_data["products"][product_id]["total"] = product_total_price(state_data=state_data)
        director.build_edit_kb(data=state_data)
        markup = builder.product.get_keyboard()
    print("=" * 100)
    pprint(await state.get_data())
    await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=markup)


@dp.callback_query_handler(edit_quantity.filter(edit="True", add="False", reduce="False"),  UpdateStateInfo())
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
        products_list[state_data.get("product_id")]['quantity'] = quantity
        products_list[state_data.get("product_id")]['total'] = product_total_price(state_data)
        director.build_edit_kb(state_data)
        markup = builder.product.get_keyboard()
        await bot.edit_message_reply_markup(inline_message_id=inline_message_id,
                                            reply_markup=markup)
        del state_data['message_data']
    pprint(await state.get_data())
    await state.reset_state(with_data=False)


@dp.callback_query_handler(edit_quantity.filter(edit="True", add="True"), UpdateStateInfo())
@dp.callback_query_handler(edit_quantity.filter(edit="True", reduce="True"), UpdateStateInfo())
async def plus_one_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get("product_id")
    async with state.proxy() as state_data:
        products_list = state_data.get("products")
        product_quantity = products_list[product_id]['quantity']
        if product_quantity == 0 and callback_data.get("reduce") == "True":
            await call.answer(text="У вас нету этого товара в корзине")
            return
        elif callback_data.get("reduce") == "True":
            products_list[product_id]['quantity'] -= 1
            await call.answer(text="Удалено из корзины")
        elif callback_data.get("add") == "True":
            products_list[product_id]['quantity'] += 1
            await call.answer(text="Добавлено в корзину")
        products_list[state_data.get("product_id")]['total'] = product_total_price(state_data)
        director.build_edit_kb(state_data)
        markup = builder.product.get_keyboard()
    await bot.edit_message_reply_markup(inline_message_id=call["inline_message_id"],
                                        reply_markup=markup)
    pprint(await state.get_data())


def product_total_price(state_data: dict):
    products_list = state_data.get("products")
    return float(products_list[state_data.get("product_id")]['quantity'] * Decimal(
        products_list[state_data.get("product_id")]['price']))


@dp.callback_query_handler(liked_product.filter(), UpdateStateInfo())
async def add_liked(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as state_data:
        if callback_data.get("delete") == "False":
            await call.answer("Добавлено в избранное")
            state_data["liked_products"].append(callback_data.get("product_id"))
        elif callback_data.get("add") == "False":
            await call.answer("Удалено из избранных")
            for count, value in enumerate(state_data['liked_products']):
                if value == callback_data.get("product_id"):
                    del state_data["liked_products"][count]
        director.build_product_kb(state_data)
        markup = builder.product.get_keyboard()
    await bot.edit_message_reply_markup(inline_message_id=call["inline_message_id"], reply_markup=markup)
    pprint(await state.get_data())

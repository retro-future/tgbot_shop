from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import buy_callback, liked_product, edit_quantity
from tgbot.keyboards.inline.gen_keyboard import director, builder, cart_edit_kb
from tgbot.loader import dp, bot
from tgbot.states.cart_states import ProductStates
from decimal import Decimal

from tgbot.utils.db_api.quick_commands import get_product


async def update_product_info(product_id: int, state: FSMContext):
    product = await get_product(product_id)
    async with state.proxy() as state_data:
        state_data["product_info"].update({
            "product_id": product.id,
            "product_title": product.title,
            "product_price": str(product.price),
            "category_id": product.parent.category_id,
            "subcategory_name": product.parent.tg_name,
        })
        if str(product.id) not in state_data['products'].keys():
            products = {
                str(product.id):
                    {
                        "title": product.title,
                        "quantity": 0,
                        "price": str(product.price),
                        "total": "0.00",
                    },
            }
            state_data['products'].update(products)
    return True


def product_total_price(state_data: dict):
    products_list = state_data.get("products")
    result = str(products_list[state_data.get("product_id")]['quantity'] * Decimal(
        products_list[state_data.get("product_id")]['price']))
    return result


@dp.callback_query_handler(buy_callback.filter())
async def add_to_cart(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get("product_id")
    await update_product_info(int(product_id), state)
    async with state.proxy() as state_data:
        state_data["product_id"] = product_id
        state_data["products"][product_id]["quantity"] += 1
        state_data["products"][product_id]["total"] = product_total_price(state_data=state_data)
        director.build_edit_kb(data=state_data)
        markup = builder.product.get_keyboard()
    print("=" * 100)
    pprint(await state.get_data())
    await bot.edit_message_reply_markup(inline_message_id=call.inline_message_id, reply_markup=markup)


@dp.callback_query_handler(edit_quantity.filter(edit="True", add="False", reduce="False"))
async def edit_product_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get("product_id")
    await update_product_info(int(product_id), state)
    await bot.send_message(chat_id=call.from_user.id, text="Введите количество товара на которую хотите изменить")
    await state.update_data(message_data=dict(call))
    await state.update_data(product_id=product_id)
    await ProductStates.QUANTITY_EDIT.set()


@dp.message_handler(state=ProductStates.QUANTITY_EDIT)
async def accept_product_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as state_data:
        quantity = int(message.text)
        products_id = state_data.get("product_id")
        inline_message_id = state_data.get("message_data")["inline_message_id"]
        products_list = state_data.get("products")
        products_list[products_id]['quantity'] = quantity
        products_list[products_id]['total'] = product_total_price(state_data)
        director.build_edit_kb(state_data)
        markup = builder.product.get_keyboard()
        await bot.edit_message_reply_markup(inline_message_id=inline_message_id,
                                            reply_markup=markup)
        del state_data['message_data']
    pprint(await state.get_data())
    await state.reset_state(with_data=False)


@dp.callback_query_handler(edit_quantity.filter(edit="True", add="True"))
@dp.callback_query_handler(edit_quantity.filter(edit="True", reduce="True"))
async def plus_one_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get("product_id")
    await update_product_info(int(product_id), state)
    async with state.proxy() as state_data:
        state_data['product_id'] = product_id
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


@dp.callback_query_handler(liked_product.filter())
async def add_liked(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get("product_id")
    await update_product_info(int(product_id), state)
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


@dp.callback_query_handler(text='show_cart')
async def show_cart(call: types.CallbackQuery, state: FSMContext):
    answer_texts = []
    total = 0
    async with state.proxy() as state_data:
        if not state_data["products"]:
            await call.answer("Корзина Пуста")
            return
        for product_id in state_data['products'].keys():
            product = state_data['products'].get(product_id)
            text = f"<b>{product['title']}</b>\n{product['quantity']} шт. x ${product['price']} = ${product['total']}\n"
            answer_texts.append(text)
            total += Decimal(product['total'])
    text = "\n".join(answer_texts)
    answer = "<b>Корзина</b>\n\n" + "----------\n" + f"{text}" + "----------\n\n" + f"<b>Итого</b>: <i>{total}$</i>"
    await call.answer()
    await bot.send_message(chat_id=call.from_user.id, text=answer, reply_markup=cart_edit_kb)


@dp.callback_query_handler(text="wipe_cart")
async def wipe_cart(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(products={})
    await call.answer()
    await bot.edit_message_text(text="Корзина очищено", chat_id=call.from_user.id,
                                message_id=call.message.message_id)


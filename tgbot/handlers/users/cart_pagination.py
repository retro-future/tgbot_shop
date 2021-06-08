from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto

from tgbot.handlers.users.cart import product_total_price, show_cart
from tgbot.keyboards.inline.callback_datas import pagination_callback, pagination_edit_callback
from tgbot.keyboards.inline.gen_keyboard import CartKeyboardGen
from tgbot.loader import dp, bot
from tgbot.states.cart_states import PaginationStates
from tgbot.utils.db_api.quick_commands import get_product


def indexed_product_id(page: int, state_data: dict):
    indexed_product_ids = dict(enumerate(state_data['products'].keys(), start=1))
    if len(indexed_product_ids) > 1:
        product_id = indexed_product_ids[page]
        return product_id
    if len(indexed_product_ids) == 1:
        return indexed_product_ids[1]


@dp.callback_query_handler(pagination_callback.filter())
async def paginate_cart_products(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    page_number = int(callback_data.get("page"))
    edit = callback_data.get("edit")
    async with state.proxy() as state_data:
        product_id = indexed_product_id(page=page_number, state_data=state_data)
        product = await get_product(product_id=int(product_id))
        cart_product = state_data['products'][str(product_id)]
        caption = cart_product['title'] + "\n\n" + str(cart_product['quantity']) + " шт. x $" + cart_product['price'] \
                  + " = $" + cart_product['total']
        keyboard = CartKeyboardGen(page=page_number, data=state_data)
        markup = keyboard.build_pagination_keyboard() if edit == "False" else keyboard.build_edit_keyboard()
        product_image = InputMediaPhoto(product.image, caption=caption)
    await call.message.edit_media(media=product_image, reply_markup=markup)


@dp.callback_query_handler(pagination_edit_callback.filter(edit="True", add="False", reduce="False"))
async def edit_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    print("hello")
    product_id = callback_data.get("product_id")
    page = int(callback_data.get("page"))
    await state.update_data(product_id=product_id)
    await state.update_data(page=page)
    await state.update_data(message_data=call.message.message_id)
    await PaginationStates.QUANTITY_EDIT.set()
    await call.message.answer(text="Введите количество товара на которую хотите изменить")


@dp.message_handler(state=PaginationStates.QUANTITY_EDIT)
async def accept_quantity(message: types.Message, state: FSMContext):
    print("hello world")
    quantity = int(message.text)
    async with state.proxy() as state_data:
        product_id = state_data.get("product_id")
        page = state_data.get("page")
        message_id = state_data.get("message_data")
        products_list = state_data.get("products")
        cart_product = products_list[str(product_id)]
        products_list[product_id]['quantity'] = quantity
        products_list[product_id]['total'] = product_total_price(state_data)
        caption = cart_product['title'] + "\n\n" + str(cart_product['quantity']) + " шт. x $" + cart_product['price'] \
                  + " = $" + cart_product['total']
        keyboard = CartKeyboardGen(page=page, data=state_data)
        markup = keyboard.build_edit_keyboard()
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=message_id, caption=caption,
                                       reply_markup=markup)
        del state_data['message_data'], state_data['page']
    await state.reset_state(with_data=False)


@dp.callback_query_handler(pagination_edit_callback.filter(reduce="True"))
async def reduce_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    page = int(callback_data.get("page"))
    product_id = callback_data.get("product_id")
    async with state.proxy() as state_data:
        product = state_data['products'][product_id]
        product['quantity'] -= 1
        if product['quantity'] == 0:
            del state_data['products'][product_id]
            page = 1
            if not state_data['products']:
                await call.message.delete()
                await call.message.answer("Корзина Пуста")
                return
            product_id = indexed_product_id(page=page, state_data=state_data)
            product = state_data['products'][product_id]
        state_data['product_id'] = product_id
        product['total'] = product_total_price(state_data)
        product_db = await get_product(product_id=int(product_id))
        caption = product['title'] + "\n\n" + str(product['quantity']) + " шт. x $" + product['price'] + " = $" + \
                  product['total']
        product_image = InputMediaPhoto(product_db.image, caption=caption)
        markup = CartKeyboardGen(page=page, data=state_data).build_edit_keyboard()
        await call.message.edit_media(media=product_image, reply_markup=markup)
        await call.answer("Успешно")


@dp.callback_query_handler(pagination_edit_callback.filter(add="True"))
async def add_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    page = int(callback_data.get("page"))
    product_id = callback_data.get("product_id")
    async with state.proxy() as state_data:
        product = state_data["products"][product_id]
        product["quantity"] += 1
        state_data["product_id"] = product_id
        product["total"] = product_total_price(state_data)
        product_db = await get_product(product_id=int(product_id))
        caption = product['title'] + "\n\n" + str(product['quantity']) + " шт. x $" + product['price'] + " = $" + \
                  product['total']
        product_image = InputMediaPhoto(product_db.image, caption=caption)
        markup = CartKeyboardGen(page=page, data=state_data).build_edit_keyboard()
        await call.message.edit_media(media=product_image, reply_markup=markup)
        await call.answer("Успешно")


@dp.callback_query_handler(text="end_edit")
async def end_editing(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await show_cart(call=call, state=state)
    await call.answer()

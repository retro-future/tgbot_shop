from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext


async def create_cart_list(state: FSMContext) -> str:
    answer_texts = []
    total = 0
    async with state.proxy() as state_data:
        for product_id in state_data['products'].keys():
            product = state_data['products'].get(product_id)
            text = f"<b>{product['title']}</b>\n{product['quantity']} шт. x ${product['price']} = ${product['total']}\n"
            answer_texts.append(text)
            total += Decimal(product['total'])
    text = "\n".join(answer_texts)
    answer = "<b>Корзина</b>\n\n" + "----------\n" + f"{text}" + "----------\n\n" + f"<b>Итого</b>: <i>{total}$</i>"
    return answer


async def check_quantity(message: types.Message) -> bool:
    try:
        quantity = int(message.text)
        if quantity > 0:
            return True
        await message.answer("Количество не может быть меньше 1, повторите попытку")
        return False
    except ValueError as e:
        await message.answer("Количество должно быть целым числом, повторите попытку")
        return False


async def gen_total_price(state: FSMContext) -> Decimal:
    async with state.proxy() as state_data:
        product_list = state_data['products']
        total = Decimal()
        for key in product_list.keys():
            price = product_list[key]["price"]
            quantity = product_list[key]["quantity"]
            total += Decimal(price) * quantity
        if not total:
            return Decimal("0.00")
    return total


async def wipe_cart_data(state: FSMContext, products: bool = False):
    field_list = ['order_id', 'order_number', 'phone_number', 'user_address', 'user_db_id']
    async with state.proxy() as state_data:
        if products:
            del state_data['products']
        for field in field_list:
            if field in state_data.keys():
                del state_data[field]

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline.callback_datas import user_address_callback, shipping_callback, payment_callback
from bot.utils.db_api.schemas.db_tables import UserAddresses


async def generate_addresses_keyboard(state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data['user_db_id']
    addresses = await UserAddresses.query.where(UserAddresses.user_id == user_id).gino.all()
    if not addresses:
        return
    keyboard = InlineKeyboardMarkup()
    for address in addresses:
        keyboard.insert(
            InlineKeyboardButton(text=address.address,
                                 callback_data=user_address_callback.new(id=address.id, name=address.address))
        )
    return keyboard


def gen_check_keyboard():
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="make_order"),
         InlineKeyboardButton(text="Нет, отмена!", callback_data="cancel_order")],
    ])
    return markup


def gen_shipping_keyboard():
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton(text="Самовывоз", callback_data=shipping_callback.new('pickup')),
         InlineKeyboardButton(text="Курьер", callback_data=shipping_callback.new('courier'))],
    ])
    return markup


def gen_payment_keyboard():
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton(text="Наличные", callback_data=payment_callback.new('cash')),
         InlineKeyboardButton(text="Карта", callback_data=payment_callback.new('card'))],
    ])
    return markup

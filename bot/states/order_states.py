from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderStates(StatesGroup):
    Address = State()
    Shipping = State()
    Payment = State()
    Phone_Number = State()

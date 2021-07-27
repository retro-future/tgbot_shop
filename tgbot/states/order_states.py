from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderStates(StatesGroup):
    Address = State()
    Phone_Number = State()
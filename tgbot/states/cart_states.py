from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductStates(StatesGroup):
    ENTRY_POINT = State()
    QUANTITY_EDIT = State()
    ACCEPT_QUANTITY = State()

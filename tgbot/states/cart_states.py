from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductStates(StatesGroup):
    QUANTITY_EDIT = State()

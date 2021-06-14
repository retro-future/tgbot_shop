from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    ENTER_REGISTRY = State()
    USER_PHONE = State()

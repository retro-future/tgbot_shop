from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from tgbot.keyboards.default.menu_kb import menu
from tgbot.loader import dp, bot
from tgbot.states.user_registration_states import RegistrationStates
from tgbot.utils.db_api.quick_commands import get_user
from tgbot.utils.db_api.schemas.goods import TgUserGino


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await state.update_data(liked_products=[])
    await state.update_data(products={})
    await state.update_data(product_info={})
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer_animation(animation="CgACAgIAAxkDAAIaWGCeQ1YMN2DcOYRBAhg7uSxe0_qnAAJtDQAC0uPwSGmwRsty71onHwQ",
                                   caption=f"Привет, {message.from_user.full_name}!", reply_markup=menu)
    await message.answer_audio(audio="CQACAgIAAxkDAAIabGCeRRsjSVkcJK_r6k1IhS-r2aatAAJwDQAC0uPwSOHahvBFJIVmHwQ")
    if not await get_user(user_id):
        async with state.proxy() as state_data:
            state_data["user_info"] = {"user_id": user_id,
                                       "name": message.from_user.full_name}
        await message.answer("Пожалуйста введите номер телефона для регистрации")
        await RegistrationStates.USER_PHONE.set()


@dp.message_handler(state=RegistrationStates.USER_PHONE)
async def register_user(message: types.Message, state: FSMContext):
    phone_number = message.text
    async with state.proxy() as state_data:
        state_data["user_info"].update({"phone_number": phone_number})
        user = await TgUserGino.create(**state_data["user_info"])
    print(user.id)
    print(user.name)
    print(user.phone_number)
    await state.reset_state(with_data=False)


@dp.message_handler(Command("reset_state"))
async def reset_my_state(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("done")


@dp.message_handler(Command("get_state"))
async def get_my_state(message: types.Message, state: FSMContext):
    pprint(await state.get_data())

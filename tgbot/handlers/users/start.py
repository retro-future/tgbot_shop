import re
from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from tgbot.keyboards.default.menu_kb import menu
from tgbot.loader import dp, bot
from tgbot.states.user_registration_states import RegistrationStates
from tgbot.utils.db_api.schemas.goods import TgUserGino

PHONE_NUMBER_PATTERN = "[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}"


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer_animation(animation="CgACAgIAAxkDAAIaWGCeQ1YMN2DcOYRBAhg7uSxe0_qnAAJtDQAC0uPwSGmwRsty71onHwQ",
                                   caption=f"Добро пожаловать, {message.from_user.full_name}!", reply_markup=menu)
    await message.answer_audio(audio="CQACAgIAAxkDAAIabGCeRRsjSVkcJK_r6k1IhS-r2aatAAJwDQAC0uPwSOHahvBFJIVmHwQ")


@dp.message_handler(Command("reset_state"))
async def reset_my_state(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("done")


@dp.message_handler(Command("get_state"))
async def get_my_state(message: types.Message, state: FSMContext):
    pprint(await state.get_data())


@dp.message_handler(state=RegistrationStates.ENTER_REGISTRY)
async def register_user(message: types.Message, state: FSMContext):
    await message.answer(f"Здраствуйте {message.from_user.full_name}, "
                         f"вам нужно зарегистрироваться чтобы пользоваться ботом")
    async with state.proxy() as state_data:
        state_data["user_info"] = {"user_id": int(message.from_user.id),
                                   "name": message.from_user.full_name}

    await message.answer("Пожалуйста введите номер телефона для регистрации")
    await RegistrationStates.USER_PHONE.set()


@dp.message_handler(state=RegistrationStates.USER_PHONE)
async def register_user(message: types.Message, state: FSMContext):
    phone_number = message.text
    result = re.search(PHONE_NUMBER_PATTERN, phone_number)
    if not result:
        await message.answer("Вы неправильно ввели номер телефона, пожалуйста введите в формате: +998*********")
        return
    async with state.proxy() as state_data:
        state_data["user_info"].update({"phone_number": result.group()})
        await TgUserGino.create(**state_data["user_info"])
        del state_data["user_info"]
    await state.reset_state(with_data=False)
    await message.answer("Чтобы начать пользоваться ботом нажмите на /start")

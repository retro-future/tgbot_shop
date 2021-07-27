import logging
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


@dp.message_handler(state=RegistrationStates.REGISTER_USER)
async def register_user(message: types.Message, state: FSMContext):
    user_id = int(message.from_user.id)
    name = message.from_user.full_name
    try:
        await TgUserGino.create(user_id=user_id, name=name)
    except Exception as err:
        logging.exception(err)
    await state.reset_state(with_data=False)
    await bot_start(message, state)

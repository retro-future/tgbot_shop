from aiogram.dispatcher.filters import Command
from aiogram import types

from tgbot.keyboards.default.menu_kb import menu
from tgbot.loader import dp
from tgbot.utils.db_api import quick_commands


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    categories = await quick_commands.show_category()
    subcategories = await quick_commands.show_subcategory()
    for i in categories:
        print(i)
    for i in subcategories:
        print(i)
    await message.answer("Pastdagi kategoriyadan birini tanlang", reply_markup=menu)

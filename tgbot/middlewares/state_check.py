from aiogram import Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline.callback_datas import parse_callback
from tgbot.utils.db_api.quick_commands import get_product


class CheckState(BaseMiddleware):
    async def check_state_data(self, user_id, chat_id):
        dp = Dispatcher.get_current()
        async with dp.current_state(chat=chat_id, user=user_id).proxy() as state_data:
            if not state_data.get("liked_products"):
                state_data["liked_products"] = []
            if not state_data.get("products"):
                state_data["products"] = {}
            if not state_data.get("product_info"):
                state_data["product_info"] = {}
        return

    async def on_pre_process_message(self, msg: Message, data: dict):
        """
        On pre_process check user state_data if it's have a keys ['liked_products', 'product_info']
        :param msg:
        :param data:
        :return:
        """
        user_id, chat_id = msg.from_user.id, msg.chat.id
        await self.check_state_data(user_id, chat_id)

    async def on_pre_process_callback_query(self, query: CallbackQuery, data: dict):
        callback_data = dict(query)
        user_id = query.from_user.id
        chat_id = callback_data["chat"]["id"] if callback_data.get("chat") else callback_data['from']['id']
        await self.check_state_data(user_id, chat_id)


class ProductInfo(BaseMiddleware):
    async def update_product_info(self, user_id, chat_id, product_id):
        dp = Dispatcher.get_current()
        async with dp.current_state(chat=chat_id, user=user_id).proxy() as state_data:
            if product_id not in state_data["products"].keys():
                product = await get_product(int(product_id))
                state_data['products'].update({
                    product_id:
                        {
                            "title": product.title,
                            "quantity": 0,
                            "price": str(product.price),
                            "total": "0.00",
                        },
                })

    async def on_pre_process_callback_query(self, query: CallbackQuery, data: dict):
        query_data = dict(query)
        callback_data = query_data.get("data")
        parsed_callback = parse_callback(callback_data)
        if not parsed_callback:
            return
        product_id = parsed_callback.get("product_id")
        user_id = query.from_user.id
        chat_id = query_data["chat"]["id"] if query_data.get("chat") else query_data['from']['id']
        await self.update_product_info(user_id=user_id, chat_id=chat_id, product_id=product_id)

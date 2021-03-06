from aiogram import Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from bot.states.user_registration_states import RegistrationStates
from bot.utils.db_api.quick_commands import get_user


class IsRegistered(BaseMiddleware):
    async def on_pre_process_message(self, msg: Message, data: dict):
        """
        On pre_process check is a user registered

        :param msg:
        :param data:
        :return:
        """
        dp = Dispatcher.get_current()
        storage = dp.storage
        user_id, chat_id = msg.from_user.id, msg.chat.id
        current_state = await storage.get_state(chat=chat_id, user=user_id)
        state_group = [state.state for state in RegistrationStates.all_states]
        user = await get_user(user_id)
        if current_state is None or current_state not in state_group:
            if not user:
                await storage.set_state(
                    chat=chat_id, user=user_id,
                    state=RegistrationStates.REGISTER_USER
                )
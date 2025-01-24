import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from database.utils import check_user_exist

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')



class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        user_id = event.from_user.id if isinstance(event, (Message, CallbackQuery)) else None

        if not user_id:
            return await handler(event, data)

        if isinstance(event, Message) and event.text == "/start":
            return await handler(event, data)
        
        if isinstance(event, Message) and event.text is None:
            return await handler(event, data)

        fsm_context: FSMContext = data.get("state")
        if fsm_context:
            state = await fsm_context.get_state()
            if state is not None and state.split(':')[0] == 'Register':
                if isinstance(event, Message) and event.text.startswith("/"):
                    await event.answer("Вы не завершили регистрацию. Пожалуйста, завершите её, чтобы продолжить.")
                    return
                return await handler(event, data)
        is_user_exist = await check_user_exist(user_id)
        if not is_user_exist:
            if isinstance(event, Message):
                await event.answer("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь ( /start ), чтобы пользоваться всеми функциями бота.")
            elif isinstance(event, CallbackQuery):
                await event.message.answer("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь ( /start ), чтобы пользоваться всеми функциями бота.")
            return

        return await handler(event, data)
    

class MainMenuMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        user_id = event.from_user.id if isinstance(event, (Message, CallbackQuery)) else None

        if not user_id:
            return await handler(event, data)

        if isinstance(event, Message) and event.text == "/start":
            return await handler(event, data)
        
        if isinstance(event, Message) and event.text is None:
            return await handler(event, data)

        fsm_context: FSMContext = data.get("state")
        if fsm_context:
            state = await fsm_context.get_state()
            if state is not None and state.split(':')[0] != 'MainMenu':
                if isinstance(event, Message) and event.text.startswith("/"):
                    await event.answer("Вы не в главном меню. Завершите действие.")
                    return
                return await handler(event, data)

        return await handler(event, data)
    
    
class LogToDatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        username = event.from_user.username
        command = event.text
        log_time = datetime.now()
        log_entry = f"{log_time} | User ID: {user_id} | Username: {username} | Command: {command}"
        logger.info(log_entry)
        return await handler(event, data)

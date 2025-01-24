import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot import bot, start_bot, scheduler
from config import Config, load_config
from handlers import start_router, main_menu_router, dynamic_router, notify_router
from handlers import blitz_router, llm_router, one_time_schedule_router, regular_schedule_router
from keyboards.main_menu import set_main_menu
from database import init_models
from middlewares import RegistrationMiddleware, LogToDatabaseMiddleware

logger = logging.getLogger(__name__)
config: Config = load_config()


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    storage: MemoryStorage = MemoryStorage()
    
    # await init_models()

    dp: Dispatcher = Dispatcher(storage=storage)
    dp.message.middleware(RegistrationMiddleware())
    dp.callback_query.middleware(RegistrationMiddleware())
    dp.message.middleware(LogToDatabaseMiddleware())
    dp.callback_query.middleware(LogToDatabaseMiddleware())
    
    dp.startup.register(start_bot)
    await set_main_menu(bot)
    dp.include_router(notify_router)
    dp.include_router(start_router)
    dp.include_router(blitz_router)
    dp.include_router(dynamic_router)
    dp.include_router(llm_router)
    dp.include_router(one_time_schedule_router)
    dp.include_router(regular_schedule_router)
    dp.include_router(main_menu_router)

    await bot.delete_webhook(drop_pending_updates=True) # убрать в продакшене
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
    finally:
        asyncio.run(bot.session.close())
        scheduler.remove_all_jobs()
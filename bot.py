import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config, load_config
from handlers import start_router, main_menu_router, dynamic_router
from handlers import blitz_router, llm_router
from keyboards.main_menu import set_main_menu
from database import init_models
from middlewares import RegistrationMiddleware

logger = logging.getLogger(__name__)

bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

async def start_bot(bot: Bot):
    pass


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    config: Config = load_config()

    storage: MemoryStorage = MemoryStorage()
    
    await init_models()

    dp: Dispatcher = Dispatcher(storage=storage)
    dp.message.middleware(RegistrationMiddleware())
    
    dp.startup.register(start_bot)
    await set_main_menu(bot)
    dp.include_router(start_router)
    dp.include_router(blitz_router)
    dp.include_router(dynamic_router)
    dp.include_router(llm_router)
    dp.include_router(main_menu_router)

    await bot.delete_webhook(drop_pending_updates=True) #убрать в продакшене
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
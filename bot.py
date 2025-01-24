import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Config, load_config

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

async def start_bot(bot: Bot):
    logger.info('Start scheduler')
    scheduler.start()
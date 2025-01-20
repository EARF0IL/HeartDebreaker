from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models import OneTimeSchedule
from bot import bot

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

async def one_time_notify(user_id, time):
    notify_info: OneTimeSchedule = await get_onetime_schedule(user_id, time)
    await bot.send_message(
        chat_id=user_id,
        text=notify_info.description
    )
    scheduler.remove_job((user_id + notify_info.time.strftime('%d.%m.%Y %H.%M')))
    
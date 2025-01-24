from database.models import OneTimeSchedule, RegularSchedule
from database.utils import get_one_time_schedule, remove_one_time_schedule
from database.utils import get_regular_schedule, remove_regular_schedule
from bot import bot
from keyboards.schedule import create_remove_job_kb_inline


async def one_time_notify(user_id, name):
    notify_info: OneTimeSchedule = await get_one_time_schedule(user_id, name)
    await bot.send_message(
        chat_id=user_id,
        text=f'*{notify_info.name}*\n{notify_info.description}'
    )
    await remove_one_time_schedule(user_id, name)
    
async def regular_notify(user_id, name):
    notify_info: RegularSchedule = await get_regular_schedule(user_id, name)
    await bot.send_message(
        chat_id=user_id,
        text=f'*{notify_info.name}*\n{notify_info.description}',
        reply_markup=create_remove_job_kb_inline(name)
    )
    # scheduler.remove_job(id=f"{user_id}+{name}")
    # await remove_one_time_schedule(user_id, name)
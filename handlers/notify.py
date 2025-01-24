from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from bot import scheduler
from database.utils import remove_regular_schedule

notify_router = Router()


@notify_router.callback_query(F.data.contains('remove'))
async def remove_regular(cb_query: CallbackQuery, state: FSMContext):
    await cb_query.message.edit_text(
        text='Напоминание удалено'
    )
    job_name = cb_query.data.split(';')[-1]
    scheduler.remove_job(
        job_id=f"{cb_query.from_user.id}+{job_name}"
    )
    await remove_regular_schedule(cb_query.from_user.id, job_name)   

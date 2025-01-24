from aiogram import Router, F
from aiogram.types import Message, Update
from aiogram.fsm.context import FSMContext
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from filters import FSMTypeFilter
from states import RegularSchedule, OneTimeSchedule
from config.text.scedules import *
from config.text import MAIN, ERR_KB
from keyboards.main_menu import create_main_menu_kb
from keyboards.blitz import *
from config.enums import *
from database.utils import add_regular_schedule
from utils import regular_notify
from bot import scheduler

regular_schedule_router = Router()
regular_schedule_router.message.filter(FSMTypeFilter(RegularSchedule))
regular_schedule_router.callback_query.filter(FSMTypeFilter(RegularSchedule))


@regular_schedule_router.message(RegularSchedule.is_regular, F.text)
async def is_regular(message: Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer(
            text=SCHEDULE_NAMING
        )
        await state.set_state(RegularSchedule.set_name)
    elif message.text == 'Нет':
        await message.answer(
            text=SCHEDULE_NAMING
        )
        await state.set_state(OneTimeSchedule.set_name)
    else:
        await message.answer(
            text=ERR_KB
        )
    


@regular_schedule_router.message(RegularSchedule.set_name, F.text)
async def set_name(message: Message, state: FSMContext):
    await message.answer(
        text=REGULAR_DESCR
    )
    await state.update_data({'name': message.text})
    await state.set_state(RegularSchedule.set_description)
    

@regular_schedule_router.message(RegularSchedule.set_description, F.text)
async def set_name(message: Message, state: FSMContext):
    await message.answer(
        text=REGULAR_SHCED
    )
    await state.update_data({'description': message.text})
    await state.set_state(RegularSchedule.set_time)
    
    
@regular_schedule_router.message(RegularSchedule.set_time, F.text)
async def set_notify(message: Message, state: FSMContext):
    try:
        dt = datetime.strptime(message.text, '%H:%M').time()
        await state.update_data({'time': dt})
        data = await state.get_data()
        await add_regular_schedule(data)
        scheduler.add_job(func=regular_notify,
                          trigger=CronTrigger(
                              hour=dt.hour,
                              minute=dt.minute
                          ),
                          args=(message.from_user.id, data['name']),
                          id=f"{data['user_id']}+{data['name']}"
                          )
        await state.clear()
        await state.set_state(None)
        await message.answer(
            text=MAIN,
            reply_markup=create_main_menu_kb(),
            show_alert=True
        )
    except ValueError as e: 
        await message.answer(
            text=TIME_ERR
        )
        raise e
        
        
@regular_schedule_router.callback_query()
@regular_schedule_router.message()
async def error_handler(update: Update, state: FSMContext):
    message: Message = update if isinstance(update, Message) else update.message 
    current_state = await state.get_state()
    match current_state:
        case _:
            await message.answer(
                text=TEXT_ERR,
                show_alert=True
            )
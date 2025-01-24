from aiogram import Router, F
from aiogram.types import Message, Update
from aiogram.fsm.context import FSMContext
from datetime import datetime

from filters import FSMTypeFilter
from states import OneTimeSchedule
from config.text.scedules import *
from config.text import MAIN
from keyboards.main_menu import create_main_menu_kb
from keyboards.blitz import *
from config.enums import *
from database.utils import add_one_time_schedule
from utils import one_time_notify
from bot import scheduler

one_time_schedule_router = Router()
one_time_schedule_router.message.filter(FSMTypeFilter(OneTimeSchedule))
one_time_schedule_router.callback_query.filter(FSMTypeFilter(OneTimeSchedule))



@one_time_schedule_router.message(OneTimeSchedule.set_name, F.text)
async def set_name(message: Message, state: FSMContext):
    await message.answer(
        text=ENTER_DESCR
    )
    await state.update_data({'name': message.text})
    await state.set_state(OneTimeSchedule.set_description)
    

@one_time_schedule_router.message(OneTimeSchedule.set_description, F.text)
async def set_name(message: Message, state: FSMContext):
    await message.answer(
        text=ENTER_DATE
    )
    await state.update_data({'description': message.text})
    await state.set_state(OneTimeSchedule.set_date)
    
    
@one_time_schedule_router.message(OneTimeSchedule.set_date, F.text)
async def set_notify(message: Message, state: FSMContext):
    try:
        dt = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        await state.update_data({'time': dt})
        data = await state.get_data()
        if dt < datetime.now():
            await message.answer(
                text=DATE_LOSE
            )
            return
        await add_one_time_schedule(data)
        scheduler.add_job(one_time_notify,
                          'date',
                          run_date=dt,
                          args=(message.from_user.id, data['name'])
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
            text=DATE_ERR
        )
        raise e
        
        
@one_time_schedule_router.callback_query()
@one_time_schedule_router.message()
async def error_handler(update: Update, state: FSMContext):
    message: Message = update if isinstance(update, Message) else update.message 
    current_state = await state.get_state()
    match current_state:
        case _:
            await message.answer(
                text=TEXT_ERR,
                show_alert=True
            )
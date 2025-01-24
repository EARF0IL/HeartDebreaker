from aiogram import Router
from aiogram.types import Message, CallbackQuery, Update, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from filters import FSMTypeFilter
from states import Blitz
from config.text.blitz import *
from keyboards.blitz import *
from keyboards import create_yes_no_kb_inline
from database.utils import check_quiz_exist, update_quiz, add_quiz, get_last_quiz

blitz_router = Router()
blitz_router.message.filter(FSMTypeFilter(Blitz))
blitz_router.callback_query.filter(FSMTypeFilter(Blitz))

@blitz_router.callback_query(Blitz.start)
async def blitz_start(cb_query: CallbackQuery, state: FSMContext):
        await state.set_state(Blitz.feeling)
        await state.update_data({'user_id': cb_query.from_user.id})
        await cb_query.message.edit_text(
            text=FEELING
        )
        await cb_query.message.edit_reply_markup(
            reply_markup=create_feelings_kb_inline()
        )
        

@blitz_router.callback_query(Blitz.feeling)
async def feeling_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'feeling': cb_query.data})
    await cb_query.message.edit_text(
        text=SYMPTOMS
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_symptoms_kb_inline()
    )
    await state.set_state(Blitz.symptoms)
    

@blitz_router.callback_query(Blitz.symptoms)
async def symptoms_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'symptoms': cb_query.data})
    await cb_query.message.edit_text(
        text=MEASURING
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_yes_no_kb_inline()
    )
    await state.set_state(Blitz.is_blood_pressure)
    
    
@blitz_router.callback_query(Blitz.is_blood_pressure)
async def is_blood_pressure_enter(cb_query: CallbackQuery, state: FSMContext):
    if cb_query.data == 'Да':
        await cb_query.message.edit_text(
            text=BLOOD_PRESSURE
        )
        await cb_query.message.edit_reply_markup(
            reply_markup=create_blood_pressure_kb_inline()
        )
        await state.set_state(Blitz.blood_pressure)
    else:
        await state.update_data({'blood_pressure': None})
        await cb_query.message.edit_text(
            text=PULSE
        )
        await cb_query.message.edit_reply_markup(
            reply_markup=create_pulse_kb_inline()
        )
        await state.set_state(Blitz.pulse)
        
        
@blitz_router.callback_query(Blitz.blood_pressure)
async def blood_pressure_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'blood_pressure': cb_query.data})
    await cb_query.message.edit_text(
        text=PULSE
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_pulse_kb_inline()
    )
    await state.set_state(Blitz.pulse)
    
    
@blitz_router.callback_query(Blitz.pulse)
async def spulse_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'pulse': cb_query.data})
    await cb_query.message.edit_text(
        text=PHYS_ACTIVITY
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_phys_activity_kb_inline()
    )
    await state.set_state(Blitz.sport)
    
    
@blitz_router.callback_query(Blitz.sport)
async def phys_activity_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'sport': cb_query.data})
    await cb_query.message.edit_text(
        text=FOOD
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_food_kb_inline()
    )
    await state.set_state(Blitz.food)
    
    
@blitz_router.callback_query(Blitz.food)
async def food_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'food': cb_query.data})
    await cb_query.message.edit_text(
        text=EMOTIONS
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_emotions_kb_inline()
    )
    await state.set_state(Blitz.emotions)
    
    
@blitz_router.callback_query(Blitz.emotions)
async def emotions_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'emotions': cb_query.data})
    await cb_query.message.edit_text(
        text=CRITICALS
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_critical_states_kb_inline()
    )
    await state.set_state(Blitz.criticals)
    

@blitz_router.callback_query(Blitz.criticals)
async def criticals_enter(cb_query: CallbackQuery, state: FSMContext):
    await state.update_data({'criticals': cb_query.data})
    await cb_query.message.edit_text(
        text=BLITZ_FINAL
    )
    await cb_query.message.edit_reply_markup(
        reply_markup=create_continue_kb_inline()
    )

    data = await state.get_data()
    
    if await check_quiz_exist(data['user_id']):
        last_quiz = await get_last_quiz(data['user_id'])
        await update_quiz(data)
    else:
        last_quiz = None
        await add_quiz(data)

    await state.update_data({'last_quiz': last_quiz})
    print(data['next_state'])
    await state.set_state(data['next_state'])
    
    
@blitz_router.callback_query()
@blitz_router.message()
async def error_handler(update: Update, state: FSMContext):
    message: Message = update if isinstance(update, Message) else update.message 
    current_state = await state.get_state()
    match current_state:
        case _:
            await message.answer(
                text=BLITZ_ERROR,
                show_alert=True
            )
    
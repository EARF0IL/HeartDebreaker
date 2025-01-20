from aiogram import Router, F
from aiogram.types import Message, Update, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters import FSMTypeFilter
from states import Dynamic, Blitz
from config.text.dynamic import *
from config.text import MAIN
from config.text.register import ERR_KB
from keyboards.main_menu import create_main_menu_kb
from keyboards.blitz import *
from config.enums import *
from database.models import LastQuiz

dynamic_router = Router()
dynamic_router.message.filter(FSMTypeFilter(Dynamic))
dynamic_router.callback_query.filter(FSMTypeFilter(Dynamic))


@dynamic_router.message(Dynamic.is_blitz, F.text)
async def is_blitz(message: Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer(
            text='*Блиц-опрос*',
            reply_markup=create_continue_kb_inline()
        )
        await state.update_data({'next_state': Dynamic.final})
        await state.set_state(Blitz.start)
    elif message.text == 'Нет':
        await message.answer(
            text=BYE
        )
        await message.answer(
            text=MAIN,
            reply_markup=create_main_menu_kb()
        )
        await state.clear()
        await state.set_state(None)
    else:
        await message.answer(
            text=ERR_KB
        )
        

@dynamic_router.callback_query(Dynamic.final)
async def final_blitz(cb_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await state.set_state(None)
    if data['is_first']:
        await cb_query.message.edit_text(
            text=FIRST_FINAL
        )
        await cb_query.message.answer(
            text=MAIN,
            reply_markup=create_main_menu_kb()
        )
    else:
        last_quiz: LastQuiz = data['last_quiz']
        print(last_quiz.feeling)
        priorities = {
            FeelingEnum.BAD.value: 0,
            FeelingEnum.OK.value: 1,
            FeelingEnum.FINE.value: 2,
            BloodPressureEnum.LOW.value: 0,
            BloodPressureEnum.NORMAL.value: 1,
            BloodPressureEnum.HIGH.value: 2,
            PulseEnum.LOW.value: 0,
            PulseEnum.MIDDLE.value: 1,
            PulseEnum.HIGH.value: 2,
            PulseEnum.NO.value: None,
            PhysActivityEnum.LOW.value: 0,
            PhysActivityEnum.MIDDLE.value: 1,
            PhysActivityEnum.HIGH.value: 2,
            FoodEnum.HUNGRY.value: 0,
            FoodEnum.HEAVY.value: 1,
            FoodEnum.LIGHT.value: 2,
            EmotionsEnum.CRITICAL.value: 0,
            EmotionsEnum.STRESS.value: 1,
            EmotionsEnum.CALM.value: 2
        }
        fill_data = {}
        
        
        if priorities[last_quiz.feeling] < priorities[data['feeling']]:
            fill_data['feeling'] = 'улучшилось'
        elif priorities[last_quiz.feeling] > priorities[data['feeling']]:
            fill_data['feeling'] = 'ухудшилось'
        else:
            fill_data['feeling'] = 'без изменений'
        
        if last_quiz.blood_pressure is None or data['blood_pressure'] is None:
            fill_data['blood_pressure'] = 'нет данных'
        elif priorities[last_quiz.blood_pressure] < priorities[data['blood_pressure']]:
            fill_data['blood_pressure'] = 'повысилось'
        elif priorities[last_quiz.blood_pressure] > priorities[data['blood_pressure']]:
            fill_data['blood_pressure'] = 'уменьшилось'
        else:
            fill_data['blood_pressure'] = 'без изменений'
            
        if priorities[last_quiz.pulse] is None or priorities[data['pulse']] is None:
            fill_data['pulse'] = 'нет данных'
        elif priorities[last_quiz.pulse] < priorities[data['pulse']]:
            fill_data['pulse'] = 'увеличился'
        elif priorities[last_quiz.pulse] > priorities[data['pulse']]:
            fill_data['pulse'] = 'уменьшился'
        else:
            fill_data['pulse'] = 'без изменений'
        
        if priorities[last_quiz.sport] < priorities[data['sport']]:
            fill_data['sport'] = 'повысился'
        elif priorities[last_quiz.sport] > priorities[data['sport']]:
            fill_data['sport'] = 'уменьшился'
        else:
            fill_data['sport'] = 'без изменений'
            
        if priorities[last_quiz.food] < priorities[data['food']]:
            fill_data['food'] = 'возросло'
        elif priorities[last_quiz.food] > priorities[data['food']]:
            fill_data['food'] = 'упало'
        else:
            fill_data['food'] = 'без изменений'
            
        if priorities[last_quiz.emotions] < priorities[data['emotions']]:
            fill_data['emotions'] = 'улучшилось'
        elif priorities[last_quiz.emotions] > priorities[data['emotions']]:
            fill_data['emotions'] = 'более тревожно'
        else:
            fill_data['emotions'] = 'стабилизировалось'
        
            
        await cb_query.message.edit_text(
            text=RESULT.format(**fill_data),
        )
        await cb_query.message.answer(
            text=MAIN,
            reply_markup=create_main_menu_kb()
        )
        
        
@dynamic_router.callback_query()
@dynamic_router.message()
async def error_handler(update: Update, state: FSMContext):
    message: Message = update if isinstance(update, Message) else update.message 
    current_state = await state.get_state()
    match current_state:
        case _:
            await message.answer(
                text=DYNAMIC_ERROR,
                show_alert=True
            )
    
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, Update
from aiogram.fsm.context import FSMContext

from config.text.register import *
from config.text.dynamic import DYNAMIC_GREET, YET_ANOTHER_BLITZ, FIRST_BLITZ
from config.text.llm_dialog import LLM_GREET
from config.text.scedules import ONE_TIME_GREET
from config.text import MAIN, HELP_MESSAGE
from states import MainMenu, Dynamic, LLMDialog, OneTimeSchedule
from keyboards import create_yes_no_kb_inline, create_yes_no_kb
from keyboards.main_menu import *
from keyboards.register import *
from config.enums import BloodPressureEnum, SportRegularityEnum
from database.utils import update_user, check_quiz_exist
from middlewares import MainMenuMiddleware

main_menu_router = Router()
main_menu_router.message.middleware(MainMenuMiddleware())


@main_menu_router.message(Command('help'), StateFilter(None))
async def help_cmd(message: Message):
    await message.answer(
        text=HELP_MESSAGE
    )
    
    await message.answer(
        text=MAIN,
        reply_markup=create_main_menu_kb()
    )


@main_menu_router.message(Command('age'), StateFilter(None))
async def age_cmd(message: Message, state: FSMContext):
    await message.answer(
        text=ASK_AGE,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainMenu.choose_age)
    
    
@main_menu_router.message(F.text, MainMenu.choose_age)
async def age_enter(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) > 0 and int(message.text) < 120:
        await message.answer(
            text='Принято.',
            reply_markup=ReplyKeyboardRemove()
        )
        await update_user({'user_id': message.from_user.id,
                           'age': int(message.text)})
        await state.set_state(None)
        await message.answer(
            text=MAIN,
            reply_markup=create_main_menu_kb()
        )
    else:
        await message.answer(
            text=ERR_AGE,
        )
        

@main_menu_router.message(Command('name'), StateFilter(None))
async def name_cmd(message: Message, state: FSMContext):
    await message.answer(
        text=ASK_NAME,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainMenu.choose_name)
    
    
@main_menu_router.message(F.text, MainMenu.choose_name)
async def age_enter(message: Message, state: FSMContext):
    await message.answer(
        text='Принято.',
        reply_markup=ReplyKeyboardRemove()
    )
    await update_user({'user_id': message.from_user.id,
                       'name': message.text})
    await state.set_state(None)
    await message.answer(
        text=MAIN,
        reply_markup=create_main_menu_kb()
        )
    
    
@main_menu_router.message(Command('heartattacks'), StateFilter(None))
async def heartattacks_cmd(message: Message, state: FSMContext):
    await message.answer(
        text=ASK_HEARTATTAK_COUNT,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainMenu.heart_attacked_count)
    
    
@main_menu_router.message(F.text, MainMenu.heart_attacked_count)
async def heartattacks_enter(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) >= 0:
        await message.answer(
            text='Принято.',
            reply_markup=ReplyKeyboardRemove()
        )
        await update_user({'user_id': message.from_user.id,
                           'heart_attacks': message.text})
        await state.set_state(None)
        await message.answer(
            text=MAIN,
            reply_markup=create_main_menu_kb()
            )
    else:
        await message.answer(
            text=ERR_HEARTATTACK_COUNT,
        )


@main_menu_router.message(Command('blood_pressure'), StateFilter(None))
async def blood_pressure_cmd(message: Message, state: FSMContext):
    await message.answer(
        text=ASK_BLOOD_PRESSURE,
        reply_markup=create_blood_pressure_kb_inline()
    )
    await state.set_state(MainMenu.choose_blood_pressure)
    
    
@main_menu_router.callback_query(F.data.in_(BloodPressureEnum.__members__.values()),
                                 MainMenu.choose_blood_pressure)
async def blood_pressure_enter(cb_query: CallbackQuery, state: FSMContext):
        await update_user({'user_id': cb_query.from_user.id,
                            'blood_pressure': cb_query.data})
        await state.set_state(None)
        await cb_query.message.delete()
        await cb_query.answer(
            text='Принято.',
            show_alert=True
        )
        
        
@main_menu_router.message(Command('smoking'), StateFilter(None))
async def blood_pressure_cmd(message: Message, state: FSMContext):
    await message.answer(
        text=SMOKING,
        reply_markup=create_yes_no_kb_inline()
    )
    await state.set_state(MainMenu.smoking)
    
    
@main_menu_router.callback_query(F.data.in_(['Да', 'Нет']), MainMenu.smoking)
async def smoking_enter(cb_query: CallbackQuery, state: FSMContext):
        await update_user({'user_id': cb_query.from_user.id,
                           'is_smoking': cb_query.data == 'Да'})
        await state.set_state(None)
        await cb_query.message.delete()
        await cb_query.answer(
            text='Принято.',
            show_alert=True
        )


@main_menu_router.message(Command('sport'), StateFilter(None))
async def blood_pressure_cmd(message: Message, state: FSMContext):
    await message.answer(
        text=SPORT,
        reply_markup=create_sport_kb_inline()
    )
    await state.set_state(MainMenu.sport)
    
    
@main_menu_router.callback_query(F.data.in_(SportRegularityEnum.__members__.values()),
                                 MainMenu.sport)
async def sport_enter(cb_query: CallbackQuery, state: FSMContext):
        await update_user({'user_id': cb_query.from_user.id,
                           'sport_regularity': cb_query.data})
        await state.set_state(None)
        await cb_query.message.delete()
        await cb_query.answer(
            text='Принято.',
            show_alert=True
        )
        
        
@main_menu_router.message(F.text == 'Динамика состояния', StateFilter(None))
async def dynamic_button(message: Message, state: FSMContext):
    await message.answer(
        text=DYNAMIC_GREET,
        reply_markup=ReplyKeyboardRemove()
    )
    if await check_quiz_exist(message.from_user.id):
        await message.answer(
            text=YET_ANOTHER_BLITZ,
            reply_markup=create_yes_no_kb()
        )
        await state.update_data({'is_first': False})
    else:
        await message.answer(
            text=FIRST_BLITZ,
            reply_markup=create_yes_no_kb()
        )
        await state.update_data({'is_first': True})
    await state.set_state(Dynamic.is_blitz)
    

@main_menu_router.message(F.text == 'Получение совета', StateFilter(None))
async def llm_button(message: Message, state: FSMContext):
    await message.answer(
        text=LLM_GREET,
        reply_markup=create_yes_no_kb()
    )

    await state.set_state(LLMDialog.is_blitz_ready)
    

@main_menu_router.message(F.text == 'Напоминание о записи', StateFilter(None))
async def onetime_schedule_button(message: Message, state: FSMContext):
    await message.answer(
        text=ONE_TIME_GREET,
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(OneTimeSchedule.set_name)


@main_menu_router.callback_query()
@main_menu_router.message()
async def error_handler(update: Update, state: FSMContext):
    message: Message = update if isinstance(update, Message) else update.message 
    current_state = await state.get_state()
    match current_state:
        case 'MainMenu:choose_name':
            await message.answer(
                text=ERR_NAME
            )
        case 'MainMenu:choose_age':
            await message.answer(
                text=ERR_AGE
            )
        case 'MainMenu:heart_attacked_count':
            await message.answer(
                text=ERR_HEARTATTACK_COUNT
            )
        case None:
            await message.answer(
                text=MAIN,
                reply_markup=create_main_menu_kb()
            )
        case _:
            await message.answer(
                text=MAIN,
                reply_markup=create_main_menu_kb(),
                show_alert=True
            )


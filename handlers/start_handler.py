from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config.text.register import *
from config.text import MAIN, HELP_MESSAGE
from states.register import Register
from keyboards import create_yes_no_kb
from keyboards.main_menu import create_main_menu_kb
from keyboards.register import *
from config.enums import BloodPressureEnum, SportRegularityEnum
from database.utils import add_user, check_user_exist, update_user
from filters import FSMTypeFilter

start_router = Router()


@start_router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text=HELP_MESSAGE,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=ASK_NAME
    )
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(Register.choosing_name)
    # TODO: add check user exist

    
@start_router.message(F.text, Register.choosing_name)
async def name_enter(message: Message, state: FSMContext):
    await message.answer(
        text=CHECK_NAME.format(USER_NAME=message.text),
        reply_markup=create_yes_no_kb()
    )
    await state.update_data(name=message.text)
    await state.set_state(Register.name_check)
    

@start_router.message(F.text, Register.name_check)
async def name_check(message: Message, state: FSMContext):
    if message.text == 'Да':
        data = await state.get_data()
        await message.answer(
            text=GREET.format(USER_NAME=data['name']),
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            text=ASK_GENDER,
            reply_markup=create_gender_kb()
        )
        await state.set_state(Register.choose_gender)
    elif message.text == 'Нет':
        await message.answer(
            text=ASK_RENAME,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Register.choosing_name)
    else:
        await message.answer(
            text=ERR_KB,
            reply_markup=ReplyKeyboardRemove()
        )


@start_router.message(F.text, Register.choose_gender)
async def gender_enter(message: Message, state: FSMContext):
    if message.text in ['Мужского', 'Женского']:
        await message.answer(
            text=ASK_AGE,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(gender=message.text.lower()[:3])
        await state.set_state(Register.choose_age)
    else:
        await message.answer(
            text=ERR_KB,
        )
        

@start_router.message(F.text, Register.choose_age)
async def age_enter(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) > 0:
        await message.answer(
            text=ASK_HEARTATTAK_COUNT,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(age=int(message.text))
        await state.set_state(Register.heart_attacked_count)
    else:
        await message.answer(
            text=ERR_AGE,
        )


@start_router.message(F.text, Register.heart_attacked_count)
async def heart_attacked_count_enter(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) >= 0:
        await message.answer(
            text=ASK_BLOOD_PRESSURE,
            reply_markup=create_blood_pressure_kb()
        )
        await state.update_data(heart_attacks=int(message.text))
        await state.set_state(Register.choose_blood_pressure)
    else:
        await message.answer(
            text=ERR_HEARTATTACK_COUNT,
        )
        
        
@start_router.message(F.text, Register.choose_blood_pressure)
async def blood_pressure_enter(message: Message, state: FSMContext):
    if message.text == 'Высокое':
        blood_pressure = BloodPressureEnum.HIGH
    elif message.text == 'Низкое':
        blood_pressure = BloodPressureEnum.LOW
    elif message.text == 'Нормальное':
        blood_pressure = BloodPressureEnum.NORMAL
    else:
        await message.answer(
            text=ERR_KB,
        )
        return
    await message.answer(
            text=SMOKING,
            reply_markup=create_yes_no_kb()
        )
    await state.update_data(blood_pressure=blood_pressure)
    await state.set_state(Register.smoking)
        

@start_router.message(F.text, Register.smoking)
async def smoking_enter(message: Message, state: FSMContext):
    if message.text in ['Да', 'Нет']:
        await message.answer(
            text=SPORT,
            reply_markup=create_sport_kb()
        )
        if message.text == 'Да':
            await state.update_data(is_smoking=True)
        else:
            await state.update_data(is_smoking=False)
        await state.set_state(Register.sport)
    else:
        await message.answer(
            text=ERR_KB,
        )
        

@start_router.message(F.text, Register.sport)
async def sport_enter(message: Message, state: FSMContext):
    if message.text == 'Часто':
        sport_regularity = SportRegularityEnum.OFTEN
    elif message.text == 'Редко':
        sport_regularity = SportRegularityEnum.RARELY
    elif message.text == 'Не занимаюсь':
        sport_regularity = SportRegularityEnum.NEVER
    else:
        await message.answer(
            text=ERR_KB,
        )
        return
    await message.answer(
        text=FINAL,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=MAIN,
        reply_markup=create_main_menu_kb()
    )
    await state.update_data(sport_regularity=sport_regularity)
    await state.set_state(None)
    data = await state.get_data()
    is_user_exist = await check_user_exist(data['user_id'])
    if is_user_exist:
        await update_user(data)
    else:
        await add_user(data)
    await state.clear()


@start_router.message(FSMTypeFilter(Register))
async def error_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    match current_state:
        case 'Register:choosing_name':
            await message.answer(
                text=ERR_NAME
            )
        case 'Register:name_check':
            await message.answer(
                text=ERR_KB
            )
        case 'Register:choose_gender':
            await message.answer(
                text=ERR_KB
            )
        case 'Register:choose_age':
            await message.answer(
                text=ERR_AGE
            )
        case _:
            await message.answer(
                text='Введите текст!'
            )
            
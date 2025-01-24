from aiogram import Router, F
from aiogram.types import Message, Update, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from filters import FSMTypeFilter, MultypleStateFilter
from states import LLMDialog, Blitz
from config.text.llm_dialog import *
from config.text import MAIN
from config.text.register import ERR_KB
from keyboards.main_menu import create_main_menu_kb
from keyboards import create_yes_no_kb
from keyboards.blitz import create_continue_kb_inline
from config.enums import *
from database.models import User
from database.utils import check_quiz_exist, get_user
from config.text import LLM_SYSTEM_MESSAGE
from LLM_io import ask_llm, get_system_prompt

llm_router = Router()
llm_router.message.filter(FSMTypeFilter(LLMDialog))
llm_router.callback_query.filter(FSMTypeFilter(LLMDialog))


@llm_router.message(LLMDialog.is_blitz_ready, F.text)
async def is_blitz(message: Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer(
            text='*Блиц-опрос*',
            reply_markup=create_continue_kb_inline()
        )
        await state.update_data({'next_state': LLMDialog.after_blitz})
        await state.set_state(Blitz.start)
    elif message.text == 'Нет':
        if not await check_quiz_exist(message.from_user.id):
            await message.answer(
                text=BYE
            )
            await message.answer(
                text=MAIN,
                reply_markup=create_main_menu_kb()
            )
            await state.clear()
            await state.set_state(None)
            return
        await message.answer(
            text=PREV_QUIZ
        )
        await message.answer(
            text=IS_PREV_QUIZ,
            reply_markup=create_yes_no_kb()
        )
        await state.set_state(LLMDialog.is_prev_result)
    else:
        await message.answer(
            text=ERR_KB
        )
        

@llm_router.message(MultypleStateFilter([LLMDialog.is_prev_result, LLMDialog.final]), F.text)
async def approve(message: Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer(
            text=ASK,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(LLMDialog.ask)
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
        
        
@llm_router.callback_query(LLMDialog.after_blitz)
async def after_blitz(cb_query: CallbackQuery, state: FSMContext):
    await cb_query.message.edit_text(
        text=ASK,
    )
    # await cb_query.message.edit_reply_markup(
    #     reply_markup=ReplyKeyboardRemove()
    # )
    await state.set_state(LLMDialog.ask)
    


@llm_router.message(LLMDialog.ask, F.text)
async def ask(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'message_history' not in data:
        user_model: User = await get_user(message.from_user.id)
        system_prompt = await get_system_prompt(dict(name=user_model.name,
                                                gender=user_model.gender.value,
                                                age=user_model.age,
                                                heartattacks=user_model.heart_attacks,
                                                blood_pressure=user_model.blood_pressure.value,
                                                is_smoked=('да' if user_model.is_smoking else 'нет'),
                                                sport_regularity=user_model.sport_regularity.value,
                                                feeling=user_model.LastQuiz.feeling.value,
                                                symptoms=user_model.LastQuiz.symptoms.value,
                                                current_blood_pressure=user_model.LastQuiz.blood_pressure.value,
                                                current_pulse=user_model.LastQuiz.pulse.value,
                                                phys_activity=user_model.LastQuiz.sport.value,
                                                food=user_model.LastQuiz.food.value,
                                                emotions=user_model.LastQuiz.emotions.value,
                                                critical_state=user_model.LastQuiz.criticals.value))
        # print(system_prompt)
        await state.update_data({'message_history': [SystemMessage(content=system_prompt.content)]})
        data = await state.get_data()
    message_history: list[dict[str, str]] = data['message_history']
    message_history.append(HumanMessage(content=message.text))
    llm_answer = await ask_llm(message_history)
    message_history.append(AIMessage(content=llm_answer))
    await message.answer(
        text=llm_answer
    )
    await message.answer(
        text=ANOTHER_QUESTIONS,
        reply_markup=create_yes_no_kb()
    )
    await state.update_data({'message_history': message_history})
    await state.set_state(LLMDialog.final)
    

@llm_router.callback_query()
@llm_router.message()
async def error_handler(update: Update, state: FSMContext):
    message: Message = update if isinstance(update, Message) else update.message 
    current_state = await state.get_state()
    match current_state:
        case _:
            await message.answer(
                text=TEXT_ERR,
                show_alert=True
            )
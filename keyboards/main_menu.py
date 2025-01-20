from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config.lexicon import MAIN_COMMANDS
from config.enums import BloodPressureEnum, SportRegularityEnum


async def set_main_menu(bot: Bot):
    main_menu = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu)
    
def create_main_menu_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(text='Получение совета'), 
        KeyboardButton(text='Динамика состояния'),
        KeyboardButton(text='Напоминание о записи'),
    )
    kb_builder.row(
        KeyboardButton(text='Напоминание лекарственное'),
        KeyboardButton(text='Викторина'),
    )
    return kb_builder.as_markup(resize_keyboard=True)

def create_blood_pressure_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Высокое', callback_data=BloodPressureEnum.HIGH.value),
        InlineKeyboardButton(text='Нормальное', callback_data=BloodPressureEnum.NORMAL.value),
        InlineKeyboardButton(text='Низкое', callback_data=BloodPressureEnum.LOW.value),
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_sport_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Часто', callback_data=SportRegularityEnum.OFTEN.value), 
        InlineKeyboardButton(text='Редко', callback_data=SportRegularityEnum.RARELY.value),
        InlineKeyboardButton(text='Не занимаюсь', callback_data=SportRegularityEnum.NEVER.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)
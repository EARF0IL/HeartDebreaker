from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_yes_no_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(text='Да'), 
        KeyboardButton(text='Нет'),
    )
    return kb_builder.as_markup(resize_keyboard=True)

def create_yes_no_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Да', callback_data='Да'), 
        InlineKeyboardButton(text='Нет', callback_data='Нет'),
    )
    return kb_builder.as_markup(resize_keyboard=True)
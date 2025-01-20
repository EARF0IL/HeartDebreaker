from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_gender_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(text='Мужского'), 
        KeyboardButton(text='Женского')
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_blood_pressure_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(text='Высокое'), 
        KeyboardButton(text='Нормальное'),
        KeyboardButton(text='Низкое')
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_sport_kb() -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(text='Часто'), 
        KeyboardButton(text='Редко'),
        KeyboardButton(text='Не занимаюсь')
    )
    return kb_builder.as_markup(resize_keyboard=True)
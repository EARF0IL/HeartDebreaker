from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_remove_job_kb_inline(name: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Удалить напоминание', callback_data=f'remove;{name}')
    )
    return kb_builder.as_markup(resize_keyboard=True)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.enums import FeelingEnum, SymptomsEnum, BloodPressureEnum, PulseEnum
from config.enums import PhysActivityEnum, FoodEnum, EmotionsEnum, CriticalStatesEnum


def create_feelings_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Отлично', callback_data=FeelingEnum.FINE.value), 
        InlineKeyboardButton(text='Удовлетворительно', callback_data=FeelingEnum.OK.value),
        InlineKeyboardButton(text='Плохо', callback_data=FeelingEnum.BAD.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_symptoms_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Дискомфорт в груди', callback_data=SymptomsEnum.DISCOMFORT.value), 
        InlineKeyboardButton(text='Головокружение', callback_data=SymptomsEnum.DIZZINESS.value),
        InlineKeyboardButton(text='Одышка или затрудненное дыхание', callback_data=SymptomsEnum.SHORTNESS.value)
    )
    kb_builder.row(
        InlineKeyboardButton(text='Усталость или слабость', callback_data=SymptomsEnum.FATIGUE.value),
        InlineKeyboardButton(text='Повышенное сердцебиение', callback_data=SymptomsEnum.RATE.value),
        InlineKeyboardButton(text='Симптомы не беспокоили', callback_data=SymptomsEnum.NO.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_blood_pressure_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Повышенное', callback_data=BloodPressureEnum.HIGH.value), 
        InlineKeyboardButton(text='Нормальное', callback_data=BloodPressureEnum.NORMAL.value),
        InlineKeyboardButton(text='Пониженное ', callback_data=BloodPressureEnum.LOW.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_phys_activity_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Минимальный', callback_data=PhysActivityEnum.LOW.value), 
        InlineKeyboardButton(text='Средний', callback_data=PhysActivityEnum.MIDDLE.value),
        InlineKeyboardButton(text='Высокий', callback_data=PhysActivityEnum.HIGH.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_food_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Легкая и сбалансированная', callback_data=FoodEnum.LIGHT.value), 
        InlineKeyboardButton(text='Жирная, соленая и тяжелая пища', callback_data=FoodEnum.HEAVY.value),
        InlineKeyboardButton(text='Давно не питался', callback_data=FoodEnum.HUNGRY.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_emotions_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Спокойное', callback_data=EmotionsEnum.CALM.value), 
        InlineKeyboardButton(text='Небольшой стресс или тревога', callback_data=EmotionsEnum.STRESS.value),
        InlineKeyboardButton(text='Очень напряженное или сильный стресс', callback_data=EmotionsEnum.CRITICAL.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_critical_states_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Потеря сознания', callback_data=CriticalStatesEnum.FAINT.value), 
        InlineKeyboardButton(text='Внезапная боль в груди или левой руке', callback_data=CriticalStatesEnum.HEARTATTACK.value),
    )
    kb_builder.row(
        InlineKeyboardButton(text='Приступ удушья или тяжелое дыхание', callback_data=CriticalStatesEnum.SUFFOCATION.value),
        InlineKeyboardButton(text='Нет, всё в порядке', callback_data=CriticalStatesEnum.NO.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_pulse_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Менее 60', callback_data=PulseEnum.LOW.value), 
        InlineKeyboardButton(text='60-100', callback_data=PulseEnum.MIDDLE.value),
    )
    kb_builder.row(
        InlineKeyboardButton(text='Более 100', callback_data=PulseEnum.HIGH.value),
        InlineKeyboardButton(text='Не могу определить', callback_data=PulseEnum.NO.value)
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_continue_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text='Продолжить', callback_data=PulseEnum.LOW.value), 
    )
    return kb_builder.as_markup(resize_keyboard=True)


def create_empty_kb_inline() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    return kb_builder.as_markup(resize_keyboard=True)
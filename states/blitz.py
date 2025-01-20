from aiogram.fsm.state import State, StatesGroup

class Blitz(StatesGroup):
    start = State()
    feeling = State()
    symptoms = State()
    is_blood_pressure = State()
    blood_pressure = State()
    pulse = State()
    sport = State()
    food = State()
    emotions = State()
    criticals = State()
from aiogram.fsm.state import State, StatesGroup

class MainMenu(StatesGroup):
    choose_age = State()
    choose_name = State()
    heart_attacked_count = State()
    choose_blood_pressure = State()
    smoking = State()
    sport = State()
from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    choosing_name = State()
    name_check = State()
    choose_gender = State()
    choose_age = State()
    heart_attacked_count = State()
    choose_blood_pressure = State()
    smoking = State()
    sport = State()
    final = State()
    
from aiogram.fsm.state import State, StatesGroup

class OneTimeSchedule(StatesGroup):
    set_name = State()
    set_description = State()
    set_date = State()
    
from aiogram.fsm.state import State, StatesGroup

class RegularSchedule(StatesGroup):
    is_regular = State()
    set_name = State()
    set_description = State()
    set_time = State()
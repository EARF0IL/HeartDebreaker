from aiogram.fsm.state import State, StatesGroup

class Dynamic(StatesGroup):
    is_blitz = State()
    final = State()
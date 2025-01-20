from aiogram.fsm.state import State, StatesGroup

class LLMDialog(StatesGroup):
    is_blitz_ready = State()
    is_prev_result = State()
    after_blitz = State()
    ask = State()
    final = State()
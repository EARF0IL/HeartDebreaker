from typing import Type
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class FSMTypeFilter(BaseFilter):
    def __init__(self, fsm: Type[StatesGroup]):
        self.fsm = fsm

    async def __call__(self, message: Message, state: FSMContext) -> bool: 
        current_state = await state.get_state()
        if current_state is None:
            return False
        state_group_name = current_state.split(':')[0]
        return state_group_name == self.fsm.__name__
    

class MultypleStateFilter(BaseFilter):
    def __init__(self, states: list[State]):
        self.states = [state.state for state in states]

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        if current_state is None:
            return False
        return current_state in self.states
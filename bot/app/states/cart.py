from aiogram.fsm.state import State, StatesGroup


class CartStates(StatesGroup):
    minus = State()
    plus = State()
    delete = State()

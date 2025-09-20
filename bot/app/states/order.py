from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_for_edit_status_order = State()


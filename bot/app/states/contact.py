from aiogram.fsm.state import State, StatesGroup


class ContactStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()
    waiting_for_delivery_method = State()

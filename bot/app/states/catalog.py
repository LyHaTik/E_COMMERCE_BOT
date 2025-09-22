from aiogram.fsm.state import State, StatesGroup


class CatalogStates(StatesGroup):
    waiting_for_product_list = State()
    waiting_for_product_details = State()
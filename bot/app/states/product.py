from aiogram.fsm.state import State, StatesGroup


class ProductStates(StatesGroup):
    waiting_for_category_name = State()
    waiting_for_product_title = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_stock = State()
    waiting_for_currency = State()
    waiting_for_img = State()
   

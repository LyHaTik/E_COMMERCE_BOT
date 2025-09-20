"""/admin — проверка прав

add_product() — шаги для добавления товара (FSM можно)

edit_product() — редактирование

delete_product() — удаление

show_orders() — список заказов

update_order_status() — изменение статуса"""
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.product import AddProduct


router = Router()


@router.message(F.text == "Добавить товар")
async def hand_add_product(message: Message, state: FSMContext):
    # Сообщение Напишите название продукта
    # state AddTask.waiting_for_product_name
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_product_title)
async def hand_add_title(message: Message, state: FSMContext):
    # state.data = title
    # Сообщение Напишите название Категория или выберите из предложенных в in-line кнопках
    # state AddTask.waiting_for_category_name
    pass

#########################################################################################    
@router.message(AddProduct.waiting_for_category_name)
async def hand_add_category(message: Message, state: FSMContext):
    # state.data = category
    # Сообщение Напишите описание продукта
    # state AddTask.waiting_for_description
    pass


@router.callback_query(AddProduct.waiting_for_category_name)
async def hand_edit_category_from_callback(callback: CallbackQuery, state: FSMContext):
    # state.data = category
    # Сообщение Напишите описание продукта
    # state AddTask.waiting_for_description
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_description)
async def hand_add_description(message: Message, state: FSMContext):
    # state.data = description
    # Сообщение Напишите стоимость продукта продукта
    # state AddTask.waiting_for_price
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_price)
async def hand_add_price(message: Message, state: FSMContext):
    # state.data = price
    # Сообщение Напишите валюту и инлайн клавиатура с вариантами валюты
    # state AddTask.waiting_for_currency
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_currency)
async def hand_add_currency(message: Message, state: FSMContext):
    # state.data = currency
    # Возврщаем сообщение Напишите кол-во, и inline 5, 10, 20, 50, 100 , 1000
    # state AddTask.waiting_for_stock
    pass


@router.callback_query(AddProduct.waiting_for_currency)
async def hand_add_currency_from_callback(callback: CallbackQuery, state: FSMContext):
    # state.data = currency
    # Возврщаем сообщение Напишите кол-во, и inline 5, 10, 20, 50, 100 , 1000
    # state AddTask.waiting_for_stock
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_stock)
async def hand_add_stock_from_text(message: Message, state: FSMContext):
    # state.data = stock
    # Соббщение Отправте фото
    # state AddProduct waiting_for_img
    pass


@router.callback_query(AddProduct.waiting_for_stock)
async def hand_add_stock_from_callback(callback: CallbackQuery, state: FSMContext):
    # state.data = stock
    # Соббщение Отправте фото
    # state AddProduct waiting_for_img
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_img)
async def hand_add_img(message: Message, state: FSMContext):
    # Соббщение Продукта и инлайн кнопки Сохранить и Отмена
    # state AddTask.waiting_for_product_status
    pass

##############################################################################################
@router.message(AddProduct.waiting_for_product_status)
async def hand_product_status(message: Message, state: FSMContext):
    # Если СОХРАНИТЬ Сохраняем товар
    # Собщение сохранения
    # Если Отменить
    # Собщение отмены
    # вызываем стартовую страницу
    # очищаем state.data и state
    pass
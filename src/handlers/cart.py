from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_menus import buy_item_cb
from src.utils.db.dbase import verification_user, empty_cart, add_to_cart


async def add_to_my_cart(callback: types.CallbackQuery, callback_data: dict):
    print(callback_data)

    customer_id = await verification_user(callback.from_user.id)
    item_id = callback_data['item_id']

    await add_to_cart(customer_id[0], item_id)
    await callback.answer("Товар добавлен")
    await callback.answer()


async def empty_my_cart(call: types.CallbackQuery, callback_data: dict):

    await empty_cart(call.from_user.id)
    await call.answer('Корзина пуста!')


def register_cart(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_my_cart, buy_item_cb.filter(action="add_to_cart"), state="*", is_user=True)
    dp.register_callback_query_handler(empty_cart, buy_item_cb.filter(action='empty'))

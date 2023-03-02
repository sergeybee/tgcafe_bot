from aiogram import types, Dispatcher
from src.keyboards.inline.ikb_products import ikb_products
from src.keyboards.inline.ikb_categories import products_cb
from src.keyboards.inline.ikb_product import back_level2


async def callback_products_category(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.edit_reply_markup(reply_markup=ikb_products(callback_data['id']))
    await callback.answer()


def register_products(dp: Dispatcher):
    dp.register_callback_query_handler(callback_products_category, products_cb.filter(action='products'),
                                       state="*", is_user=True)
    dp.register_callback_query_handler(callback_products_category, back_level2.filter(action='back_level2'), state="*",
                                       is_user=True)

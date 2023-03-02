from aiogram import types, Dispatcher
from src.keyboards.inline.ikb_products import back_level, ikb_products
from src.keyboards.inline.ikb_categories import categories_cb


async def callback_products_category(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.edit_text("Товары", reply_markup=ikb_products(callback_data['id']))
    await callback.answer()


def register_products(dp: Dispatcher):
    dp.register_callback_query_handler(callback_products_category, categories_cb.filter(action='categories'),
                                       state="*", is_user=True)
    dp.register_callback_query_handler(callback_products_category, back_level.filter(action='back_level2'), state="*",
                                       is_user=True)

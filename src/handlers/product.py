from aiogram import types, Dispatcher
from src.keyboards.inline.ikb_product import ikb_product, back_level2
from src.keyboards.inline.ikb_products import product_cb

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)


async def callback_product_page(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.edit_text("Товар", reply_markup=ikb_product(callback, callback_data['id']))
    await callback.answer()


def register_product(dp: Dispatcher):
    dp.register_callback_query_handler(callback_product_page, product_cb.filter(action='product'), state="*",
                                       is_user=True)



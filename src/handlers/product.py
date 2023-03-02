from aiogram import types, Dispatcher
from src.keyboards.inline.ikb_product import ikb_product
from src.keyboards.inline.ikb_products import products_cb

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)


async def callback_product_page(callback: types.CallbackQuery, callback_data: dict):
    print(callback_data)
    await callback.message.edit_text("Товар", reply_markup=ikb_product())
    await callback.answer()


def register_product(dp: Dispatcher):
    dp.register_callback_query_handler(callback_product_page, products_cb.filter(action='products'), state="*",
                                       is_user=True)


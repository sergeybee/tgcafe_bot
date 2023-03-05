from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_menus import buy_item
from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)


async def add_to_cart(callback: types.CallbackQuery, callback_data: dict):
    id_user = db.verification_user(callback.from_user.id)
    product_id = int(callback_data['item_id'])

    await db.add_to_cart(id_user[0], product_id)
    await callback.answer("Товар добавлен")
    await callback.answer()


def register_cart(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_cart, buy_item.filter(), state="*", is_user=True)

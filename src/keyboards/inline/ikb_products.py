from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

products_cb = CallbackData('products', 'id', 'action')
back_level = CallbackData('back', 'action')


# Inline кнопки с продуктами категории
def ikb_products(category_id):
    products = db.get_products(category_id)
    markup = InlineKeyboardMarkup()
    for idx, name, price in products:
        markup.add(
            InlineKeyboardButton(f"{name} {price} руб.", callback_data=products_cb.new(id=idx, action="products")))

    markup.add(InlineKeyboardButton(text="Назад", callback_data=back_level.new(action='back_level1')))
    return markup

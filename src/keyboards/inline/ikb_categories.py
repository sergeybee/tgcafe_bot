from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

products_cb = CallbackData('products', 'id', 'action')


# Inline кнопки с категориями (после нажатия Меню)
def ikb_categories():
    categories = db.get_categories()
    markup = InlineKeyboardMarkup()
    for idx, name in categories:
        markup.add(InlineKeyboardButton(name, callback_data=products_cb.new(id=idx, action="products")))

    return markup

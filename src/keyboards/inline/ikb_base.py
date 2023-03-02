from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

product_cd = CallbackData('product', 'id', 'action')


# Inline кнопка добавления в корзину
def ikb_add_product_to_cart():
    global product_cb

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Добавить в корзину - {price}₽', callback_data=product_cd.new(id=idx, action='add')))

    return markup


def ikb_empty_order_cart(idx=''):
    global product_cb

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f'Подтвердить заказ', callback_data=product_cd.new(id=idx, action='add')))

    return markup




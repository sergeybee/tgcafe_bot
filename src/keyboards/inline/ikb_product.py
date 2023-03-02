from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.keyboards.inline.ikb_base import ikb_add_product_to_cart

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

product_cb = CallbackData('product', 'action')
back_level = CallbackData('back', 'action')


# Inline кнопки увеличения кол-ва товаров в карточке или корзине
def ikb_product():
    global products_cb

    markup = InlineKeyboardMarkup()
    decr_btn = InlineKeyboardButton(text="-", callback_data=product_cb.new(action="decrease"))
    count_btn = InlineKeyboardButton(text="1", callback_data=product_cb.new(action="count"))
    incr_btn = InlineKeyboardButton(text="+", callback_data=product_cb.new(action="increase"))
    back_btn = InlineKeyboardButton(text="Назад", callback_data=back_level.new(action="back_level2"))
    markup.add(decr_btn, count_btn, incr_btn, back_btn)

    return markup

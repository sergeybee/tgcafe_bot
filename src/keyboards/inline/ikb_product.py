from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.utils.callback_data import CallbackData

# from src.keyboards.inline.ikb_base import ikb_add_product_to_cart

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

item = CallbackData('item', 'action')
back_level2 = CallbackData('back_level2', 'action')


# Inline кнопки увеличения кол-ва товаров в карточке или корзине
def ikb_product(call, product_id):
    global products_cb

    product = db.get_product(product_id)
    print(product)
    call.message.answer(product)

    markup = InlineKeyboardMarkup()
    decr_btn = InlineKeyboardButton(text="-", callback_data=item.new(action="decrease"))
    count_btn = InlineKeyboardButton(text="1", callback_data=item.new(action="count"))
    incr_btn = InlineKeyboardButton(text="+", callback_data=item.new(action="increase"))
    back_btn = InlineKeyboardButton(text="Назад", callback_data=back_level2.new(action="back_level2"))
    markup.add(decr_btn, count_btn, incr_btn, back_btn)

    return markup

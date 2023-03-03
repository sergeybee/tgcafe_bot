from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

menu_cd = CallbackData("show_menu", "level", "category_id", "item_id")
buy_item = CallbackData("buy", "item_id")


def make_callback_data(level, category_id="0", item_id="0"):
    return menu_cd.new(level=level, category_id=category_id, item_id=item_id)


# LEVEL 1 - Категории. Inline кнопки с категориями (после нажатия Меню)
def ikb_categories():
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    categories = db.get_categories()
    for category_id, name in categories:

        # Сформируем текст, который будет на кнопке
        btn_name = f"{name}"

        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category_id=category_id)
        markup.add(InlineKeyboardButton(text=btn_name, callback_data=callback_data))

    return markup


# LEVEL 2 - Продукты категории. Inline кнопки с продуктами категории
def ikb_products(category_id):
    CURRENT_LEVEL = 2

    products = db.get_products(category_id)
    markup = InlineKeyboardMarkup()
    for item_id, name, price in products:
        # Сформируем текст, который будет на кнопке
        btn_name = f"{name} {price} руб."

        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, item_id=item_id, category_id=category_id)
        markup.add(InlineKeyboardButton(text=btn_name, callback_data=callback_data))

    markup.row(InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)))
    return markup


# LEVEL 3 - Карточка товара. Inline кнопки увеличения кол-ва товаров в карточке или корзине
def ikb_product(category_id, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=f"Купить", callback_data=buy_item.new(item_id=item_id)))
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category_id=category_id)))
    return markup

    # decr_btn = InlineKeyboardButton(text="-", callback_data=item.new(action="decrease"))
    # count_btn = InlineKeyboardButton(text="1", callback_data=item.new(action="count"))
    # incr_btn = InlineKeyboardButton(text="+", callback_data=item.new(action="increase"))
    # back_btn = InlineKeyboardButton(text="Назад", callback_data=back_level2.new(action="back_level2"))
    # markup.add(decr_btn, count_btn, incr_btn, back_btn)
    #
    # return markup


# def cart_menu():
#     btn_place = InlineKeyboardButton('Оформить заказ на', callback_data='place_order') # + srt (sum)
#     '''
#     btn_left = InlineKeyboardButton('<', callback_data='left') # flipping
#     btn_quantity = InlineKeyboardButton('', callback_data='quantity') # to add pages
#     btn_right = InlineKeyboardButton('>', callback_data='right')
#     '''
#     btn_empty_cart = InlineKeyboardButton('Очистить', callback_data='empty')
#     btn_back_cart = InlineKeyboardButton('К товарам', callback_data='back_cart')
#
#     markup_cart = InlineKeyboardMarkup(row_width=1)
#     markup_cart.add(btn_place, btn_empty_cart, btn_back_cart)
#
#     return markup_cart

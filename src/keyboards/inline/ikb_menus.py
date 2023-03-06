from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

menu_cd = CallbackData("show_menu", "level", "category_id", "item_id")
buy_item_cd = CallbackData("buy", "item_id")
incr_decr_btn = CallbackData("amount_item", "action")


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

    # Кнопки плюс (+), кол-во товара (0-100) и кнопка минус (-)
    decr_btn = InlineKeyboardButton(text="-", callback_data=incr_decr_btn.new(action="decrease"))
    count_btn = InlineKeyboardButton(text="1", callback_data=incr_decr_btn.new(action="count"))
    incr_btn = InlineKeyboardButton(text="+", callback_data=incr_decr_btn.new(action="increase"))
    markup.row(decr_btn, count_btn, incr_btn)

    # Кнопка "Добавить в корзину"
    markup.row(InlineKeyboardButton(text=f"Добавить в корзину", callback_data=buy_item_cd.new(item_id=item_id)))

    # Кнопка "Назад"
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category_id=category_id)))
    return markup


# def cart_menu():
#     btn_place = InlineKeyboardButton('Оформить заказ', callback_data=cart_cb.new('place_order'))  # + srt (sum)
#     '''
#     btn_left = InlineKeyboardButton('<', callback_data='left') # flipping
#     btn_quantity = InlineKeyboardButton('', callback_data='quantity') # to add pages
#     btn_right = InlineKeyboardButton('>', callback_data='right')
#     '''
#     btn_empty_cart = InlineKeyboardButton('Очистить', callback_data=cart_cb.new('empty'))
#     btn_back_cart = InlineKeyboardButton('Назад к товарам', callback_data=cart_cb.new('back_cart'))
#
#     markup_cart = InlineKeyboardMarkup(row_width=1)
#     markup_cart.add(btn_place, btn_empty_cart, btn_back_cart)
#
#     return markup_cart


# async def gen_products(data, user_id):
#     keyboard = InlineKeyboardMarkup()
#     for i in data:
#         count = await db.get_count_in_cart(user_id, i[1])
#         count = 0 if not count else sum(j[0] for j in count)
#         keyboard.add(InlineKeyboardButton(text=f'{i[2]}: {i[3]}p - {count}шт',
#                                           callback_data=f'btn:plus:{i[1]}:{i[5]}'))
#         keyboard.add(InlineKeyboardButton(text='🔽', callback_data=f'btn:minus:{i[1]}:{i[5]}'),
#                      InlineKeyboardButton(text='🔼', callback_data=f'btn:plus:{i[1]}:{i[5]}'),
#                      InlineKeyboardButton(text='❌', callback_data=f'btn:del:{i[1]}:{i[5]}'))
#     keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:-:-'))
#
#     return keyboard

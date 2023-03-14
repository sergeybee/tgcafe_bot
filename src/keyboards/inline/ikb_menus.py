from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.utils.db.dbase import get_categories, get_products, get_count_in_cart

menu_cb = CallbackData("show_menu", "level", "category_id", "item_id")
buy_item_cb = CallbackData("buy", "item_id", "action")
quantity_item_cb = CallbackData("quantity_item", "category_id", "item_id", "quantity", "action")
cart_cb = CallbackData("cart_menu", "quantity")


def make_callback_data(level, category_id=0, item_id=0):
    return menu_cb.new(level=level, category_id=category_id, item_id=item_id)


async def ikb_categories() -> InlineKeyboardMarkup:
    """ LEVEL 1 - Категории. Inline кнопки с категориями (после нажатия на ReplyBtn "Меню") """

    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    categories = await get_categories()

    for category_id, name in categories:

        # Формируем текст, который будет на кнопке
        btn_name = f"{name}"

        # Формируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category_id=category_id)
        markup.add(InlineKeyboardButton(text=btn_name, callback_data=callback_data))

    return markup


async def ikb_products(category_id: int) -> InlineKeyboardMarkup:
    """ LEVEL 2 - Выводит список продуктов категории Inline кнопками """

    CURRENT_LEVEL = 2

    products = await get_products(category_id)
    markup = InlineKeyboardMarkup()
    for item_id, name, price in products:

        # Формируем текст, который будет на кнопке
        btn_name = f"{name} {price} руб."

        # Формируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, item_id=item_id, category_id=category_id)
        markup.add(InlineKeyboardButton(text=btn_name, callback_data=callback_data))

    markup.row(InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)))
    return markup


async def ikb_product(category_id: int, item_id: int, quantity: int) -> InlineKeyboardMarkup:
    """ LEVEL 3 - Карточка товара. Inline кнопки увеличения кол-ва товаров в карточке """

    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()

    decr_btn = InlineKeyboardButton(text="-", callback_data=quantity_item_cb.new(action="decr", category_id=category_id,
                                                                                 item_id=item_id, quantity=quantity))
    count_btn = InlineKeyboardButton(text=str(quantity), callback_data="quantity_text")
    incr_btn = InlineKeyboardButton(text="+", callback_data=quantity_item_cb.new(action="incr", category_id=category_id,
                                                                                 item_id=item_id, quantity=quantity))
    markup.row(decr_btn, count_btn, incr_btn)

    # Кнопка "Добавить в корзину"
    markup.row(InlineKeyboardButton(text=f"Добавить в корзину", callback_data=buy_item_cb.new(action="add_to_cart",
                                                                                              item_id=item_id)))

    # Кнопка "Назад"
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category_id=category_id)))
    return markup


async def ikb_cart(data, customer_id):

    keyboard = InlineKeyboardMarkup()
    for i in data:
        count = await get_count_in_cart(customer_id, i[1])
        count = 0 if not count else sum(j[0] for j in count)
        keyboard.add(InlineKeyboardButton(text=f'{i[2]}: {i[3]}p - {count}шт',
                                          callback_data=f'btn:plus:{i[1]}:{i[5]}'))
        keyboard.add(InlineKeyboardButton(text='🔽', callback_data=f'btn:minus:{i[1]}:{i[5]}'),
                     InlineKeyboardButton(text='🔼', callback_data=f'btn:plus:{i[1]}:{i[5]}'),
                     InlineKeyboardButton(text='❌', callback_data=f'btn:del:{i[1]}:{i[5]}'))

    btn_place = InlineKeyboardButton('Оформить заказ', callback_data=cart_cb.new('place_order'))  # + srt (sum)

    btn_empty_cart = InlineKeyboardButton('Очистить', callback_data=cart_cb.new('empty'))
    btn_back_cart = InlineKeyboardButton('Назад к товарам', callback_data=cart_cb.new(level=1))

    markup_cart = InlineKeyboardMarkup(row_width=1)
    markup_cart.add(btn_place, btn_empty_cart, btn_back_cart)

    return markup_cart

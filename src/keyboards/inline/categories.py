from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


# Меню категорий продуктов
def categories():
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Супы', callback_data='sups')
            ],
            [
                InlineKeyboardButton(text='Каши', callback_data='cashi')
            ]
            ,
            [
                InlineKeyboardButton(text='Чаи, Кофе', callback_data='tea')
            ],
            [
                InlineKeyboardButton(text='Пироги', callback_data='pirogi')
            ]
        ]
    )

    return inline_kb

# # 2 level: all products
# def products_menu():
#     markup_categ = InlineKeyboardMarkup(row_width=1)
#     btn_incr = InlineKeyboardButton('+', callback_data='incr')
#     btn_decr = InlineKeyboardButton('-', callback_data='decr')
#     for product in db.show_products():
#         #markup_categ.add(InlineKeyboardButton(product[1], callback_data='product_id' + str(product[0])))
#         markup_categ.row(btn_decr, btn_incr)
#     markup_categ.add(InlineKeyboardButton('Назад', callback_data='back_product'))

#     return markup_categ

# '''pr_cb = CallbackData('product', 'id', 'action')
# def test_out(idx = '', price = 0):
#     global pr_cb
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton(f'add to cart - {price}rub', callback_data=pr_cb.new(id = idx, action = 'add')))
#     return markup'''


# category_cb = CallbackData('category', 'id', 'action')


# def categories_markup():

#     global category_cb

#     markup = InlineKeyboardMarkup()
#     for idx, title in db.fetchall('SELECT * FROM categories'):
#         markup.add(InlineKeyboardButton(title, callback_data=category_cb.new(id=idx, action='view')))

#     return markup

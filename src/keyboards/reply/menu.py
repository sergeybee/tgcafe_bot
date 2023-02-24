from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



back_message = '👈 Назад'
confirm_message = '✅ Подтвердить заказ'
all_right_message = '✅ Все верно'
cancel_message = '🚫 Отменить'


def show_menu():

    reply_menu = ReplyKeyboardMarkup(
        keyboard=[
        [
        KeyboardButton(text='Меню'),
        KeyboardButton(text='Корзина')
        ],
        [
        KeyboardButton(text='Мои заказы'),
        KeyboardButton(text='Помощь')
        ]
        ],
        resize_keyboard=True)
    return reply_menu


def confirm_order_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(confirm_message)
    markup.add(back_message)

    return markup

def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(back_message)

    return markup

def check_order_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(back_message, all_right_message)

    return markup

def submit_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(cancel_message, all_right_message)

    return markup

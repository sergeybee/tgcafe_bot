from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    adm_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Посмотреть статистику'),
                KeyboardButton(text='Добавить товар')
            ],
            [
                KeyboardButton(text='Редактировать товар'),
            ]
        ],
        resize_keyboard=True)
    return adm_menu


def statistics_menu():
    report_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отчет за сегодня'),
                KeyboardButton(text='Отчет за неделю')
            ],
            [
                KeyboardButton(text='Отчет за месяц'),
                KeyboardButton(text='Назад')
            ]
        ],
        resize_keyboard=True)
    return report_menu

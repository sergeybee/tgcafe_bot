from aiogram import types, Dispatcher
from src.keyboards.reply.menu_admin import admin_menu, statistics_menu
from src.utils.db.psgql import show_users


async def admin_start(message: types.Message):
    await message.answer("Hello, admin!", reply_markup=admin_menu())
    await message.delete()


async def show_statistics(message: types.Message):
    await message.answer(f"Выбери что ты хотел! {show_users(message)}", reply_markup=statistics_menu())
    await message.delete()


async def back_in_general_menu(message: types.Message):
    await message.answer('Назад',   reply_markup=admin_menu())
    await message.delete()


async def add_product_process(message: types.Message):
    text = [
        "По вопросам предзаказа можно обратиться по тел. +7(111)111-11-11. "
        "Если у вас возникла проблема или вопрос по работе с ботом, вы можете обратиться @adress_tp."
    ]
    await message.answer('Назад'.join(text))
    await message.delete()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(show_statistics, text="Посмотреть статистику", state="*", is_admin=True)
    dp.register_message_handler(back_in_general_menu, text="Назад", state="*", is_admin=True)

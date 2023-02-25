from aiogram import types, Dispatcher

from src.keyboards.reply.menu_user import show_user_menu
from src.keyboards.inline.categories import categories


async def user_start(message: types.Message):
    await message.answer("Hello, user!", reply_markup=show_user_menu())
    await message.delete()


async def show_categories(message: types.Message):
    await message.answer("Hello, user! Ознакомьтесь с нашим меню!", reply_markup=categories())
    await message.delete()


async def show_help(message: types.Message):
    text = [
        "По вопросам предзаказа можно обратиться по тел. +7(111)111-11-11. "
        "Если у вас возникла проблема или вопрос по работе с ботом, вы можете обратиться @adress_tp."
    ]
    await message.answer('\n'.join(text))
    await message.delete()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*", is_user=True)
    dp.register_message_handler(show_categories, text="Меню", state="*", is_user=True)
    dp.register_message_handler(show_help, text="Помощь")

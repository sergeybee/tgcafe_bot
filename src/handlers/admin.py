from aiogram import Dispatcher
from aiogram.types import Message
from src.keyboards.reply.menu import show_menu
from src.keyboards.inline.categories import categories
import time


async def admin_start(message: Message):
    await message.answer("Hello, admin!", reply_markup=show_menu())
    time.sleep(1)
    await message.delete()


async def show_categories(message: Message):
    await message.answer("Ознакомьтесь с нашим меню", reply_markup=categories())
    time.sleep(1)
    await message.delete()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(show_categories, text="Меню", state="*", is_admin=True)  


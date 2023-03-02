from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_cart import cart_menu


async def message_handler_cart(message: types.Message):
    await message.answer(f"Корзина товаров:", reply_markup=cart_menu())
    await message.delete()


def register_cart(dp: Dispatcher):
    dp.register_message_handler(message_handler_cart, text="Корзина", state="*", is_user=True)

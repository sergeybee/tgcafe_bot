import datetime

from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_menus import ikb_cart
from src.keyboards.reply.menu_user import user_menu

from datetime import datetime
from src.utils.db.dbase import verification_user, add_new_user, get_my_cart


async def message_handler_user_start(message: types.Message):
    """ Проверяем существование пользователя в БД, если его нет то создаем его"""

    global first_name, user_name
    user_id = await verification_user(message.from_user.id)

    if not user_id:
        await message.answer("Здравствуйте, вы у нас в первый раз!?", reply_markup=user_menu())

        if message.from_user.first_name != "None":
            first_name = message.from_user.first_name
        elif message.from_user.username != "None":
            user_name = message.from_user.username

        await add_new_user(message.from_user.id, first_name, user_name, datetime.now())

    else:
        await message.bot.send_message(message.chat.id, "Рады видеть вас снова!!!", reply_markup=user_menu())

    await message.delete()


async def message_handler_show_help(message: types.Message):
    """ Хендлер на получение справочной информации """

    text = [
        "По вопросам предзаказа можно обратиться по тел. +7(111)111-11-11. "
        "Если у вас возникла проблема или вопрос по работе с ботом, вы можете обратиться @adress_tp."
    ]
    await message.answer('\n'.join(text))
    await message.delete()


async def message_handler_my_cart(message: types.Message):
    """ Хендлер на получение товаров из корзины """
    customer_id = await verification_user(message.from_user.id)
    item_list_my_cart = await get_my_cart(customer_id[0])
    markup = await ikb_cart(item_list_my_cart, customer_id)
    if customer_id is not None and item_list_my_cart is not None:

        await message.answer(f"Ваша корзина: {item_list_my_cart} :)", reply_markup=markup)

    else:
        await message.answer("В корзине пока нет товаров:")
    await message.delete()


async def message_handler_my_order(message: types.Message):
    """ Хендлер на отображение всех сделанных заказов """

    if not verification_user(message.from_user.id):
        await message.answer("У вас нет заказов")
    else:
        await message.answer("Ваши заказы, здесь будут выводиться заказы. Нужно только сформировать запрос к БД :)")
    await message.delete()


def register_user(dp: Dispatcher):
    dp.register_message_handler(message_handler_user_start, commands=["start"], state="*", is_user=True)
    dp.register_message_handler(message_handler_show_help, text="Помощь")
    dp.register_message_handler(message_handler_my_cart, text="Корзина")
    dp.register_message_handler(message_handler_my_order, text="Мои заказы")

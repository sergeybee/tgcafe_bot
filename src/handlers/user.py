import datetime

from aiogram import types, Dispatcher

from src.keyboards.reply.menu_user import user_menu

from datetime import datetime
from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)


async def message_handler_user_start(message: types.Message):
    #     """welcome message."""
    #     if await db.verification(message.from_user.id):
    #         await bot.send_message(message.chat.id, "👋 Hello, I remember you.")
    #     else:
    #         if message.from_user.first_name != "None":
    #             name = message.from_user.first_name
    #         elif message.from_user.username != "None":
    #             name = message.from_user.username
    #         elif message.from_user.last_name != "None":
    #             name = message.from_user.last_name
    #         else:
    #             name = ""
    #         await db.add_user(message.from_user.id, name, message.from_user.locale.language_name)
    #         await bot.send_message(message.chat.id, "ℹ️ <b>[About]\n</b> Bot is a template for future projects.")

    if not db.verification_user(message.from_user.id):
        await message.answer("Здравствуйте, вы у нас в первый раз", reply_markup=user_menu())
        db.add_new_user(message.from_user.id, message.from_user.first_name, message.from_user.username,
                        datetime.now())
    else:
        await message.answer("Рады видеть вас снова!!!", reply_markup=user_menu())
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

    id_user = db.verification_user(message.from_user.id)
    # res = db.get_my_cart(id_user[0])
    # print(res)
    #
    if not db.get_my_cart(id_user[0]):
        await message.answer("В корзине нет товаров:")
    else:
        await message.answer("Ваша корзина: Тут ваши товары. Нужно только правильно сформировать запрос :)")
    await message.delete()


async def message_handler_my_order(message: types.Message):
    """ Хендлер на отображение всех сделанных заказов """

    if not db.verification_user(message.from_user.id):
        await message.answer("У вас нет заказов")
    else:
        await message.answer("Ваши заказы, здесь будут выводиться заказы. Нужно только сформировать запрос к БД :)")
    await message.delete()


def register_user(dp: Dispatcher):
    dp.register_message_handler(message_handler_user_start, commands=["start"], state="*", is_user=True)
    dp.register_message_handler(message_handler_show_help, text="Помощь")
    dp.register_message_handler(message_handler_my_cart, text="Корзина")
    dp.register_message_handler(message_handler_my_order, text="Мои заказы")

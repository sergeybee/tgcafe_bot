import datetime

from aiogram import types, Dispatcher

from src.keyboards.reply.menu_user import user_menu

from src.handlers.categories import message_handler_categories

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

    if not db.exists_user(message.from_user.id):
        await message.answer("Здравствуйте, вы у нас в первый раз", reply_markup=user_menu())
        db.create_new_user(message.from_user.id, message.from_user.first_name, message.from_user.username,
                           datetime.now())
    else:
        await message.answer("Рады видеть вас снова!!!", reply_markup=user_menu())
    await message.delete()


async def message_handler_show_help(message: types.Message):

    text = [
            "По вопросам предзаказа можно обратиться по тел. +7(111)111-11-11. "
            "Если у вас возникла проблема или вопрос по работе с ботом, вы можете обратиться @adress_tp."
        ]
    await message.answer('\n'.join(text))
    await message.delete()


def register_user(dp: Dispatcher):
    dp.register_message_handler(message_handler_user_start, commands=["start"], state="*", is_user=True)
    dp.register_message_handler(message_handler_categories, text="Меню", state="*", is_user=True)
    dp.register_message_handler(message_handler_show_help, text="Помощь")

from typing import Union

from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_menus import ikb_categories, ikb_products, ikb_product
from src.keyboards.inline.ikb_menus import menu_cd

from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)


async def msg_call_handler_list_categories(message: Union[types.CallbackQuery, types.Message], **kwargs):
    if isinstance(message, types.Message):
        await message.answer(f"Выберите раздел, чтобы вывести список товаров:", reply_markup=ikb_categories())

    elif isinstance(message, types.CallbackQuery):
        callback = message
        await callback.message.edit_reply_markup(reply_markup=ikb_categories())


async def callback_list_products(callback: types.CallbackQuery, category_id, **kwargs):

    await callback.message.edit_reply_markup(reply_markup=ikb_products(category_id))
    await callback.answer()


async def callback_show_product(callback: types.CallbackQuery, category_id, item_id):
    await callback.message.edit_text(f"Товар: {db.get_product(item_id)}", reply_markup=ikb_product(category_id, item_id))
    await callback.answer()


async def navigate(callback: types.CallbackQuery, callback_data: dict):
    """
    :param callback: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    print(callback)
    print(callback_data)

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category_id = callback_data.get("category_id")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    item_id = int(callback_data.get("item_id"))

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "1": msg_call_handler_list_categories,  # Отдаем категории
        "2": callback_list_products,  # Отдаем товары
        "3": callback_show_product  # Предлагаем купить товар
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        callback,
        category_id=category_id,
        item_id=item_id
    )


def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(msg_call_handler_list_categories, text="Меню", state="*", is_user=True)
    dp.register_callback_query_handler(navigate, menu_cd.filter(), state="*", is_user=True)
    # dp.register_callback_query_handler(msg_call_handler_list_categories, back_level1.filter(action='back_level1'), state="*",
    #                                    is_user=True)
    # dp.register_callback_query_handler(callback_list_products, menu_cd.filter(level=2),
    #                                    state="*", is_user=True)
    # dp.register_callback_query_handler(callback_list_products, back_level2.filter(action='back_level2'), state="*",
    #                                    is_user=True)
    # dp.register_callback_query_handler(callback_show_product, product_cb.filter(action='product'), state="*",
    #                                    is_user=True)

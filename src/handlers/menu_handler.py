from typing import Union

from aiogram import types, Dispatcher
# from aiogram.types import InputFile

from src.keyboards.inline.ikb_menus import ikb_categories, ikb_products, ikb_product, quantity_item_cb
from src.keyboards.inline.ikb_menus import menu_cb
from src.utils.db.dbase import get_product, get_photo_item


async def msg_call_list_categories(message: Union[types.CallbackQuery, types.Message], **kwargs):
    if isinstance(message, types.Message):
        markup_categories = await ikb_categories()
        await message.answer(f"Выберите раздел:", reply_markup=markup_categories)

    elif isinstance(message, types.CallbackQuery):
        callback = message
        markup_categories = await ikb_categories()
        await callback.message.edit_reply_markup(reply_markup=markup_categories)


# async def callback_list_products(callback: types.CallbackQuery, category_id, **kwargs):
async def callback_list_products(callback: types.CallbackQuery, callback_data: dict):
    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category_id = callback_data.get("category_id")
    markup_products = await ikb_products(category_id)
    await callback.message.edit_reply_markup(reply_markup=markup_products)
    await callback.answer()


async def callback_show_product(callback: types.CallbackQuery, callback_data: dict):
    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category_id = callback_data.get("category_id")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    item_id = callback_data.get("item_id")

    if callback_data.get("action") == 'incr':
        # Получаем количество товара из клавиатуры
        quantity_value = int(callback_data.get("quantity"))
        quantity_value = quantity_value + 1
        markup = await ikb_product(category_id, item_id, quantity_value)
        await callback.message.edit_reply_markup(reply_markup=markup)
        await callback.answer()

    elif callback_data.get("action") == 'decr':
        # Получаем количество товара из клавиатуры
        quantity_value = int(callback_data.get("quantity"))
        quantity_value = quantity_value - 1
        markup = await ikb_product(category_id, item_id, quantity_value)
        await callback.message.edit_reply_markup(reply_markup=markup)
        await callback.answer()

    product = await get_product(item_id)
    product_photo = await get_photo_item(item_id)
    # product_photo = InputFile("path/img0.jpg")

    name = product[0]
    description = product[1]
    price = product[2]

    text = (f"<b>{name}</b>\n"
            f"\n"
            f"{description:}\n"
            f"\n"
            f"<b>Цена: \t{price:} руб. </b>\n")

    await callback.bot.send_photo(callback.from_user.id, product_photo[0])
    markup_item = await ikb_product(category_id, item_id, 1)

    await callback.message.answer(text, reply_markup=markup_item)

    await callback.answer()


# async def callbacks_num_change_increase(call: types.CallbackQuery, callback_data: dict):
#     # Получаем категорию, которую выбрал пользователь (Передается всегда)
#     category_id = callback_data.get("category_id")
#
#     # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
#     item_id = callback_data.get("item_id")
#
#     # Получаем количество товара из клавиатуры
#     quantity_value = int(callback_data.get("quantity"))
#
#     quantity_value = quantity_value + 1
#
#     markup = await ikb_product(category_id, item_id, quantity_value)
#     await call.message.edit_reply_markup(reply_markup=markup)
#     await call.answer()


# async def callbacks_num_change_decrease(call: types.CallbackQuery, callback_data: dict):
#     # Получаем категорию, которую выбрал пользователь (Передается всегда)
#     category_id = callback_data.get("category_id")
#
#     # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
#     item_id = callback_data.get("item_id")
#
#     # Получаем количество товара из клавиатуры
#     quantity_value = int(callback_data.get("quantity"))
#
#     quantity_value = quantity_value - 1
#
#     markup = await ikb_product(category_id, item_id, quantity_value)
#     await call.message.edit_reply_markup(reply_markup=markup)
#     await call.answer()


def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(msg_call_list_categories, text="Меню", state="*", is_user=True)
    dp.register_callback_query_handler(msg_call_list_categories, menu_cb.filter(level='1'), state="*", is_user=True)
    dp.register_callback_query_handler(callback_list_products, menu_cb.filter(level='2'), state="*", is_user=True)
    dp.register_callback_query_handler(callback_show_product, menu_cb.filter(level='3'), state="*", is_user=True)
    dp.register_callback_query_handler(callback_show_product, quantity_item_cb.filter(action='incr'), state="*",
                                       is_user=True)
    dp.register_callback_query_handler(callback_show_product, quantity_item_cb.filter(action='decr'), state="*",
                                       is_user=True)

from typing import Union

from aiogram import types, Dispatcher
from src.keyboards.inline.ikb_products import back_level, ikb_products
from src.keyboards.inline.ikb_categories import ikb_categories, categories_cb


async def message_handler_categories(message: Union[types.CallbackQuery, types.Message], **kwargs):
    if isinstance(message, types.Message):
        await message.answer(f"Выберите раздел, чтобы вывести список товаров:", reply_markup=ikb_categories())

    elif isinstance(message, types.CallbackQuery):
        callback = message
        await callback.message.edit_reply_markup(reply_markup=ikb_categories())


def register_categories(dp: Dispatcher):
    dp.register_callback_query_handler(message_handler_categories, back_level.filter(action='back_level1'), state="*",
                                       is_user=True)
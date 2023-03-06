from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_menus import buy_item_cd
from src.utils.db.dbase import DataBase
from src.config import load_config

config = load_config(".env")
db = DataBase(config.db.database, config.db.user, config.db.password, config.db.host)

# Формирует список товаров в корзине
# async def gen_products(data, user_id):
#     keyboard = InlineKeyboardMarkup()
#     for i in data:
#         count = await db.get_count_in_cart(user_id, i[1])
#         count = 0 if not count else sum(j[0] for j in count)
#         keyboard.add(InlineKeyboardButton(text=f'{i[2]}: {i[3]}p - {count}шт',
#                                           callback_data=f'btn:plus:{i[1]}:{i[5]}'))
#         keyboard.add(InlineKeyboardButton(text='🔽', callback_data=f'btn:minus:{i[1]}:{i[5]}'),
#                      InlineKeyboardButton(text='🔼', callback_data=f'btn:plus:{i[1]}:{i[5]}'),
#                      InlineKeyboardButton(text='❌', callback_data=f'btn:del:{i[1]}:{i[5]}'))
#     keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:-:-'))
#
#     return keyboard


async def add_to_cart(callback: types.CallbackQuery, callback_data: dict):
    id_user = db.verification_user(callback.from_user.id)
    product_id = int(callback_data['item_id'])

    await db.add_to_cart(id_user[0], product_id)
    await callback.answer("Товар добавлен")
    await callback.answer()


async def empty_cart(call: types.CallbackQuery, callback_data: dict):

    await db.empty_cart(call.from_user.id)
    await call.answer('Корзина пуста!')


def register_cart(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_cart, buy_item_cd.filter(), state="*", is_user=True)
    # dp.register_callback_query_handler(empty_cart, buy_item.filter(action='empty'))

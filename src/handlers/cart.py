from aiogram import types, Dispatcher

from src.keyboards.inline.ikb_cart import cart_menu


async def message_handler_cart(message: types.Message):
    await message.answer(f"Корзина товаров:", reply_markup=cart_menu())
    await message.delete()


def register_cart(dp: Dispatcher):
    dp.register_message_handler(message_handler_cart, text="Корзина", state="*", is_user=True)


# from aiogram.types import Message, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
#     LabeledPrice
# from aiogram.dispatcher.filters import Command
# from aiogram.types.message import ContentType
# from aiogram.utils.callback_data import CallbackData
#
# from src.services import DataBase
# from src.bot import dp, bot
# from src.config import Config
#
# cb = CallbackData('btn', 'type', 'product_id', 'category_id')
# db = DataBase('tgbot_database.db')
#
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
#
# @dp.message_handler(Command('shop'))
# async def shop(message: Message):
#     data = await db.get_categories()
#     keyboard = InlineKeyboardMarkup()
#     for i in data:
#         keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))
#
#     await message.answer('Что хотите купить?', reply_markup=keyboard)
#
# @dp.callback_query_handler(cb.filter(type='category'))
# async def goods(call: CallbackQuery, callback_data: dict):
#     data = await db.get_products(callback_data.get('category_id'))
#     keyboard = await gen_products(data, call.message.chat.id)
#
#     await call.message.edit_reply_markup(keyboard)
#
# @dp.callback_query_handler(cb.filter(type='back'))
# async def back(call: CallbackQuery):
#     data = await db.get_categories()
#     keyboard = InlineKeyboardMarkup()
#     for i in data:
#         keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:category:-:{i[1]}'))
#
#     await call.message.edit_reply_markup(keyboard)
#
# @dp.callback_query_handler(cb.filter(type='minus'))
# async def minus(call: CallbackQuery, callback_data: dict):
#     product_id = callback_data.get('product_id')
#     count_in_cart = await db.get_count_in_cart(call.message.chat.id, product_id)
#     if not count_in_cart or count_in_cart[0][0] == 0:
#         await call.message.answer('Товар в  корзине отсутсвует!')
#         return 0
#     elif count_in_cart[0][0] == 1:
#         await db.remove_one_item(product_id, call.message.chat.id)
#     else:
#         await db.change_count(count_in_cart[0][0] - 1, product_id, call.message.chat.id)
#
#     data = await db.get_products(callback_data.get('category_id'))
#     keyboard = await gen_products(data, call.message.chat.id)
#
#     await call.message.edit_reply_markup(keyboard)
#
# @dp.callback_query_handler(cb.filter(type='plus'))
# async def plus(call: CallbackQuery, callback_data: dict):
#     product_id = callback_data.get('product_id')
#     count_in_cart = await db.get_count_in_cart(call.message.chat.id, product_id)
#     count_in_stock = await db.get_count_in_stock(product_id)
#     if count_in_stock[0][0] == 0:
#         await call.message.answer('Товара нет в наличии :(')
#         return 0
#     elif not count_in_cart or count_in_cart[0][0] == 0:
#         await db.add_to_cart(call.message.chat.id, product_id)
#         await call.message.answer('Добавил!')
#     elif count_in_cart[0][0] < count_in_stock[0][0]:
#         await db.change_count(count_in_cart[0][0] + 1, product_id, call.message.chat.id)
#     else:
#         await call.message.answer('Больше нет в наличии')
#         return 0
#
#     data = await db.get_products(callback_data.get('category_id'))
#     keyboard = await gen_products(data, call.message.chat.id)
#
#     await call.message.edit_reply_markup(keyboard)
#
# @dp.callback_query_handler(cb.filter(type='del'))
# async def delete(call: CallbackQuery, callback_data: dict):
#     product_id = callback_data.get('product_id')
#     count_in_cart = await db.get_count_in_cart(call.message.chat.id, product_id)
#     if not count_in_cart:
#         await call.message.answer('Товар в корзине отсутствует!')
#         return 0
#     else:
#         await db.remove_one_item(product_id, call.message.chat.id)
#
#     data = await db.get_products(callback_data.get('category_id'))
#     keyboard = await gen_products(data, call.message.chat.id)
#
#     await call.message.edit_reply_markup(keyboard)
#
# @dp.message_handler(Command('empty'))
# async def empty_cart(message: Message):
#     await db.empty_cart(message.chat.id)
#     await message.answer('Корзина пуста!')
#
# # @dp.callback_query_handler(cb.filter(type='buy'))
# # async def add_to_cart(call: CallbackQuery, callback_data: dict):
# #     await call.answer(cache_time=30)
# #
# #     user_id = call.message.chat.id
# #     product_id = callback_data.get('id')
# #
# #     await db.add_to_cart(user_id, product_id)
# #     await call.message.answer('Добавил!')
#
# @dp.message_handler(Command('pay'))
# async def buy(message: Message):
#     data = await db.get_cart(message.chat.id)
#     new_data = []
#     for i in range(len(data)):
#         new_data.append(await db.get_user_product(data[i][2]))
#     new_data = [new_data[i][0] for i in range(len(new_data))]
#     prices = [LabeledPrice(label=new_data[i][2]+f' x {data[i][3]}',
#                            amount=new_data[i][3]*100*data[i][3]) for i in range(len(new_data))]
#     await bot.send_invoice(message.chat.id,
#                            title='Cart',
#                            description='Description',
#                            provider_token=Config.pay_token,
#                            currency='rub',
#                            need_email=True,
#                            prices=prices,
#                            start_parameter='example',
#                            payload='some_invoice')
#
# @dp.pre_checkout_query_handler(lambda q: True)
# async def checkout_process(pre_checkout_query: PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def s_pay(message: Message):
#     await db.empty_cart(message.chat.id)
#     await bot.send_message(message.chat.id, 'Платеж прошел успешно!!!')
#
#
#     -----------------------------------------
#     import logging
#     from aiogram.dispatcher import FSMContext
#     from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
#         InlineKeyboardButton
#     from keyboards.inline.products_from_cart import product_markup, product_cb
#     from aiogram.utils.callback_data import CallbackData
#     from keyboards.default.markups import *
#     from aiogram.types.chat import ChatActions
#     from states import CheckoutState
#     from loader import dp, db, bot
#     from filters import IsUser
#     from .menu import cart
#
#     @dp.message_handler(IsUser(), text=cart)
#     async def process_cart(message: Message, state: FSMContext):
#
#         cart_data = db.fetchall(
#             'SELECT * FROM cart WHERE cid=?', (message.chat.id,))
#
#         if len(cart_data) == 0:
#
#             await message.answer('Ваша корзина пуста.')
#
#         else:
#
#             await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
#             async with state.proxy() as data:
#                 data['products'] = {}
#
#             order_cost = 0
#
#             for _, idx, count_in_cart in cart_data:
#
#                 product = db.fetchone('SELECT * FROM products WHERE idx=?', (idx,))
#
#                 if product == None:
#
#                     db.query('DELETE FROM cart WHERE idx=?', (idx,))
#
#                 else:
#                     _, title, body, image, price, _ = product
#                     order_cost += price
#
#                     async with state.proxy() as data:
#                         data['products'][idx] = [title, price, count_in_cart]
#
#                     markup = product_markup(idx, count_in_cart)
#                     text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price}₽.'
#
#                     await message.answer_photo(photo=image,
#                                                caption=text,
#                                                reply_markup=markup)
#
#             if order_cost != 0:
#                 markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#                 markup.add('📦 Оформить заказ')
#
#                 await message.answer('Перейти к оформлению?',
#                                      reply_markup=markup)
#
#     @dp.callback_query_handler(IsUser(), product_cb.filter(action='count'))
#     @dp.callback_query_handler(IsUser(), product_cb.filter(action='increase'))
#     @dp.callback_query_handler(IsUser(), product_cb.filter(action='decrease'))
#     async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
#
#         idx = callback_data['id']
#         action = callback_data['action']
#
#         if 'count' == action:
#
#             async with state.proxy() as data:
#
#                 if 'products' not in data.keys():
#
#                     await process_cart(query.message, state)
#
#                 else:
#
#                     await query.answer('Количество - ' + data['products'][idx][2])
#
#         else:
#
#             async with state.proxy() as data:
#
#                 if 'products' not in data.keys():
#
#                     await process_cart(query.message, state)
#
#                 else:
#
#                     data['products'][idx][2] += 1 if 'increase' == action else -1
#                     count_in_cart = data['products'][idx][2]
#
#                     if count_in_cart == 0:
#
#                         db.query('''DELETE FROM cart
#                         WHERE cid = ? AND idx = ?''', (query.message.chat.id, idx))
#
#                         await query.message.delete()
#                     else:
#
#                         db.query('''UPDATE cart
#                         SET quantity = ?
#                         WHERE cid = ? AND idx = ?''', (count_in_cart, query.message.chat.id, idx))
#
#                         await query.message.edit_reply_markup(product_markup(idx, count_in_cart))
#
#     @dp.message_handler(IsUser(), text='📦 Оформить заказ')
#     async def process_checkout(message: Message, state: FSMContext):
#
#         await CheckoutState.check_cart.set()
#         await checkout(message, state)
#
#     async def checkout(message, state):
#         answer = ''
#         total_price = 0
#
#         async with state.proxy() as data:
#             for title, price, count_in_cart in data['products'].values():
#                 tp = count_in_cart * price
#                 answer += f'<b>{title}</b> * {count_in_cart}шт. = {tp}₽\n'
#                 total_price += tp
#
#         await message.answer(f'{answer}\nОбщая сумма заказа: {total_price}₽.',
#                              reply_markup=check_markup())
#
#     @dp.message_handler(IsUser(), lambda message: message.text not in [all_right_message, back_message],
#                         state=CheckoutState.check_cart)
#     async def process_check_cart_invalid(message: Message):
#         await message.reply('Такого варианта не было.')
#
#     @dp.message_handler(IsUser(), text=back_message, state=CheckoutState.check_cart)
#     async def process_check_cart_back(message: Message, state: FSMContext):
#         await state.finish()
#         await process_cart(message, state)
#
#     @dp.message_handler(IsUser(), text=all_right_message, state=CheckoutState.check_cart)
#     async def process_check_cart_all_right(message: Message, state: FSMContext):
#         await CheckoutState.next()
#         await message.answer('Укажите свое имя.',
#                              reply_markup=back_markup())
#
#     @dp.message_handler(IsUser(), text=back_message, state=CheckoutState.name)
#     async def process_name_back(message: Message, state: FSMContext):
#         await CheckoutState.check_cart.set()
#         await checkout(message, state)
#
#     @dp.message_handler(IsUser(), state=CheckoutState.name)
#     async def process_name(message: Message, state: FSMContext):
#
#         async with state.proxy() as data:
#
#             data['name'] = message.text
#
#             if 'address' in data.keys():
#
#                 await confirm(message)
#                 await CheckoutState.confirm.set()
#
#             else:
#
#                 await CheckoutState.next()
#                 await message.answer('Укажите свой адрес места жительства.',
#                                      reply_markup=back_markup())
#
#     @dp.message_handler(IsUser(), text=back_message, state=CheckoutState.address)
#     async def process_address_back(message: Message, state: FSMContext):
#
#         async with state.proxy() as data:
#             await message.answer('Изменить имя с <b>' + data['name'] + '</b>?',
#                                  reply_markup=back_markup())
#
#         await CheckoutState.name.set()
#
#     @dp.message_handler(IsUser(), state=CheckoutState.address)
#     async def process_address(message: Message, state: FSMContext):
#
#         async with state.proxy() as data:
#             data['address'] = message.text
#
#         await confirm(message)
#         await CheckoutState.next()
#
#     async def confirm(message):
#
#         await message.answer('Убедитесь, что все правильно оформлено и подтвердите заказ.',
#                              reply_markup=confirm_markup())
#
#     @dp.message_handler(IsUser(), lambda message: message.text not in [confirm_message, back_message],
#                         state=CheckoutState.confirm)
#     async def process_confirm_invalid(message: Message):
#         await message.reply('Такого варианта не было.')
#
#     @dp.message_handler(IsUser(), text=back_message, state=CheckoutState.confirm)
#     async def process_confirm(message: Message, state: FSMContext):
#
#         await CheckoutState.address.set()
#
#         async with state.proxy() as data:
#             await message.answer('Изменить адрес с <b>' + data['address'] + '</b>?',
#                                  reply_markup=back_markup())
#
#     @dp.message_handler(IsUser(), text=confirm_message, state=CheckoutState.confirm)
#     async def process_confirm(message: Message, state: FSMContext):
#
#         enough_money = True  # enough money on the balance sheet
#         markup = ReplyKeyboardRemove()
#
#         if enough_money:
#
#             logging.info('Deal was made.')
#
#             async with state.proxy() as data:
#
#                 cid = message.chat.id
#                 products = [idx + '=' + str(quantity)
#                             for idx, quantity in db.fetchall('''SELECT idx, quantity FROM cart
#                 WHERE cid=?''', (cid,))]  # idx=quantity
#
#                 db.query('INSERT INTO orders VALUES (?, ?, ?, ?)',
#                          (cid, data['name'], data['address'], ' '.join(products)))
#
#                 db.query('DELETE FROM cart WHERE cid=?', (cid,))
#
#                 await message.answer('Ок! Ваш заказ уже в пути 🚀\nИмя: <b>' + data['name'] + '</b>\nАдрес: <b>' + data[
#                     'address'] + '</b>',
#                                      reply_markup=markup)
#         else:
#
#             await message.answer('У вас недостаточно денег на счете. Пополните баланс!',
#                                  reply_markup=markup)
#
#         await state.finish()
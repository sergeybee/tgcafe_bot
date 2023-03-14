import datetime

import psycopg2

from src.config import load_config

config = load_config(".env")
connect = psycopg2.connect(database=config.db.database, user=config.db.user, password=config.db.password, host=config.db.host)
cursor = connect.cursor()


async def verification_user(tg_id: int):
    """ Проверяет наличие пользователя в БД """
    with connect:
        cursor.execute('SELECT id, tg_id FROM customers WHERE tg_id=%s', (tg_id,))
        result = cursor.fetchone()
    return result


async def add_new_user(tg_id: int, name: str, nick_name: str, create_date: datetime):
    """ Создает нового пользователя в БД """
    with connect:
        cursor.execute('INSERT INTO customers(tg_id, name, nick_name, create_date) VALUES(%s, %s, %s, %s)',
                            (tg_id, name, nick_name, create_date,))


async def get_categories():
    """ Получает все категории 1-го уровня """
    with connect:
        cursor.execute('SELECT id, name FROM category')
        result = cursor.fetchall()
    return result


async def get_products(category_id):
    """ Получает все продукты категории из 1-го уровня """
    with connect:
        cursor.execute('SELECT id, name, price FROM product WHERE category_id=%s', (category_id,))

        result = cursor.fetchall()
    return result


async def get_product(item_id):
    """ Получает информацию о продукте из списка продуктов уровня """
    with connect:
        cursor.execute('SELECT name, description, price FROM product WHERE id=%s', (item_id,))
        result = cursor.fetchone()
    return result


async def get_photo_item(item_id):
    """ Получает фотографию продукта """
    with connect:
        cursor.execute('SELECT url FROM product_photo WHERE product_id=%s', (item_id,))
        result = cursor.fetchone()
    return result


async def add_to_cart(customer_id: int, product_id: int):
    """ Добавляет товар в корзину """
    with connect:
        return cursor.execute('INSERT INTO cart(customers_id, product_id) VALUES(%s, %s)', (customer_id, product_id,))


async def get_my_cart(customer_id: int) -> list:
    """ Выводит все товары из корзины """
    with connect:
        cursor.execute('SELECT * FROM cart WHERE customers_id=%s', (customer_id,))

        result = cursor.fetchall()
    return result


async def get_count_in_cart(customer_id: int, item_id: int) -> list:
    """ Выводит все товары из корзины """
    with connect:
        cursor.execute('SELECT count FROM cart WHERE customers_id=%s AND item_id=%s', (customer_id, item_id,))

        result = cursor.fetchall()
    return result


async def remove_one_item(customer_id: int, item_id: int) -> None:
    """ Удаляет товар из корзины """
    with connect:
        return cursor.execute('DELETE FROM cart WHERE customers_id=%s AND item_id=%s', (customer_id, item_id,))


async def change_count(count: int, customer_id: int, item_id: int) -> None:
    """ Удаляет товар из корзины """
    with connect:
        return cursor.execute('UPDATE cart SET count=%s WHERE customers_id=%s AND item_id=%s', (count, customer_id, item_id,))


async def get_my_orders(user_id):
    """ Выводит все заказы если они есть (были) """
    with connect:
        cursor.execute('SELECT * FROM order WHERE user_id=%s', (user_id,))

        result = cursor.fetchall()
    return result


async def empty_cart(user_id):
    """ Очищает корзину """
    with connect:
        return cursor.execute('DELETE FROM cart WHERE customer_id=%s', (user_id,))

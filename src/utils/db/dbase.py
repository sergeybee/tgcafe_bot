import datetime

import psycopg2


class DataBase:
    def __init__(self, database, user, password, host):
        self.connect = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.cursor = self.connect.cursor()

    def verification_user(self, tg_id):
        """ Проверяет наличие пользователя в БД """
        with self.connect:
            self.cursor.execute('SELECT tg_id FROM customers WHERE tg_id=%s', (tg_id,))
            result = self.cursor.fetchone()
        return result

    def add_new_user(self, tg_id: int, name: str, nick_name: str, create_date: datetime):
        """ Создает нового пользователя в БД """
        with self.connect:
            self.cursor.execute('INSERT INTO customers(tg_id, name, nick_name, create_date) VALUES(%s, %s, %s, %s)',
                                (tg_id, name, nick_name, create_date,))

    def get_categories(self):
        """ Получает все категории 1-го уровня """
        with self.connect:
            self.cursor.execute('SELECT id, name FROM category')
            result = self.cursor.fetchall()
        return result

    def get_products(self, category_id):
        """ Получает все продукты категории из 1-го уровня """
        with self.connect:
            self.cursor.execute('SELECT id, name, price FROM product WHERE category_id=%s', (category_id,))

            result = self.cursor.fetchall()
        return result

    def get_product(self, product_id):
        """ Получает информацию о продукте из списка продуктов уровня """
        with self.connect:
            #self.cursor.execute('SELECT id, name, price FROM product WHERE id=%s', (product_id,))
            self.cursor.execute('SELECT product.id, product.name, product.description, product.price, product_photo.url FROM product_photo JOIN product ON product_photo.product_id = product.id')
            result = self.cursor.fetchone()
        return result

    def add_to_cart(self, user_id, product_id, count):
        """ Добавляет товар в корзину """
        with self.connect:
            self.cursor.execute('INSERT INTO cart(user_id) VALUES(%s), (user_id)')

            result = self.cursor.fetchone()
        return result

    def get_my_cart(self, user_id):
        """ Выводит все товары из корзины """
        with self.connect:
            self.cursor.execute('SELECT * FROM order WHERE user_id=%s', (user_id,))

            result = self.cursor.fetchall()
        return result

    def get_my_orders(self, user_id):
        """ Выводит все заказы если они есть (были) """
        with self.connect:
            self.cursor.execute('SELECT * FROM order WHERE user_id=%s', (user_id,))

            result = self.cursor.fetchall()
        return result

    def empty_cart(self, user_id):
        """ Очищает корзину """
        with self.connect:
            return self.cursor.execute('DELETE FROM cart WHERE user_id=%s', (user_id,))

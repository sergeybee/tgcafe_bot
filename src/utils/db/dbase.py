import datetime

import psycopg2


class DataBase:
    def __init__(self, database, user, password, host):
        self.connect = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.cursor = self.connect.cursor()

    def exists_user(self, tg_id):
        """Проверяет наличие пользователя в БД"""
        with self.connect:
            self.cursor.execute('SELECT tg_id FROM customers WHERE tg_id=%s', (tg_id,))
            result = self.cursor.fetchone()
        return result

    def create_new_user(self, tg_id: int, name: str, nick_name: str, create_date: datetime):
        # self.cursor.execute("""INSERT INTO users (user_id, name, role) VALUES (?, ?, ?)""",
        #                     [user_id, name, 'admin' if user_id == Config.admin_ids else 'user'])
        """Создает нового пользователя в БД
        tg_id: id пользователя ТГ
        name: имя пользователя
        nick_name: никнейм пользователя в ТГ
        create_date: дата создания в БД
        """
        with self.connect:
            self.cursor.execute('INSERT INTO customers(tg_id, name, nick_name, create_date) VALUES(%s, %s, %s, %s)', (tg_id, name, nick_name, create_date,))

    def get_categories(self):
        """Получает все категории 1-го уровня"""
        with self.connect:
            self.cursor.execute('SELECT id, name FROM category')
            result = self.cursor.fetchall()
        return result

    def get_products(self, category_id):
        """Получает все продукты категории из 1-го уровня"""
        with self.connect:
            self.cursor.execute('SELECT id, name, price FROM product WHERE category_id=%s', (category_id,))

            result = self.cursor.fetchall()
        return result

    async def get_product(self, product_id):
        """Получает информацию о продукте из списка продуктов уровня"""
        with self.connect:
            self.cursor.execute('SELECT id, name, price FROM product WHERE id=%s', (product_id,))

            result = self.cursor.fetchone()
        return result


    # async def add_user(self, user_id: int, name: str, lang: str) -> None:
    #     """add a new user to the database."""
    #     await self.pool.execute(f"INSERT INTO Users VALUES({user_id}, '{name}', '{lang}')")
    #     logger.info(f"added new user | user_id: {user_id}; name: {name}; language: {lang}")
    #
    # async def verification(self, user_id: int) -> bool:
    #     """checks if the user is in the database."""
    #     response = await self.pool.fetchrow(f"SELECT EXISTS(SELECT user_id FROM Users WHERE user_id={user_id})")
    #     return True if response else False


    # ------- Сделать здесь --------------------

    # async def get_cart(self, user_id):
    #     with self.connect:
    #         return self.cursor.execute("""SELECT * FROM cart WHERE user_id=(?)""", [user_id]).fetchall()
    #
    # async def add_to_cart(self, user_id, product_id):
    #     with self.connect:
    #         return self.cursor.execute("""INSERT INTO cart (user_id, product_id, count) VALUES (?, ?, ?)""",
    #                                    [user_id, product_id, 1])
    #
    # async def empty_cart(self, user_id):
    #     with self.connect:
    #         return self.cursor.execute("""DELETE FROM cart WHERE user_id=(?)""", [user_id])
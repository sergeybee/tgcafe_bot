import psycopg2

from src.config import Config




# async def update_label(self, label, user_id):
#     with self.connect:
#         return self.cursor.execute("""UPDATE users SET label=(?) WHERE user_id=(?)""",
#                                    [label, user_id])
#
# async def get_payment_status(self, user_id):
#     with self.connect:
#         return self.cursor.execute("""SELECT bought, label FROM users WHERE user_id=(?)""",
#                                    [user_id]).fetchall()
#
# async def update_payment_status(self, user_id):
#     with self.connect:
#         return self.cursor.execute("""UPDATE users SET bought=(?) WHERE user_id=(?)""",
#                                    [True, user_id])


# async def get_count_in_cart(self, user_id, product_id):
#     with self.connect:
#         return self.cursor.execute("""SELECT count FROM cart WHERE user_id=(?) AND product_id=(?)""",
#                                    [user_id, product_id]).fetchall()
#
# async def get_count_in_stock(self, product_id):
#     with self.connect:
#         return self.cursor.execute("""SELECT count FROM products WHERE product_id=(?)""",
#                                    [product_id]).fetchall()
#
# async def remove_one_item(self, product_id, user_id):
#     with self.connect:
#         return self.cursor.execute("""DELETE FROM cart WHERE product_id=(?) AND user_id=(?)""",
#                                    [product_id, user_id])

# async def change_count(self, count, product_id, user_id):
#     with self.connect:
#         return self.cursor.execute("""UPDATE cart SET count=(?) WHERE product_id=(?) AND user_id=(?)""",
#                                    [count, product_id, user_id])
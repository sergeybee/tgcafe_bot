import psycopg2
from psycopg2.extras import Json, DictCursor

from src.config import Config


def show_users(obj):
    try:
        config: Config = obj.bot.get('config')
        conn = psycopg2.connect(
            database=config.db.database,
            user=config.db.user,
            password=config.db.password,
            host=config.db.host
        )

        with conn.cursor() as cursor:

            cursor.execute('SELECT * FROM users LIMIT 5')
            get_users = cursor.fetchall()
            return get_users

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


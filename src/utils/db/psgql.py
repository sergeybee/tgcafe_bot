import psycopg2
from psycopg2.extras import Json, DictCursor

from src.config import Config


def show_users(obj):
    config: Config = obj.bot.get('config')
    conn = psycopg2.connect(
        database=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host
    )

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

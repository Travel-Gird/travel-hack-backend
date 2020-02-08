import psycopg2
from psycopg2.extras import RealDictCursor

import config


data = {}


def upload_places_to_db(data):
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASSWORD,
                            host=config.DB_HOST,
                            port=config.DB_PORT,
                            cursor_factory=RealDictCursor)
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO places (title, image, time_shift, description) VALUES ('{timeline}')")


if __name__ == '__main__':
    upload_places_to_db(data)

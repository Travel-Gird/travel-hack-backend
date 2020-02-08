import psycopg2
from psycopg2.extras import RealDictCursor

import local_config


def get_places_from_db():
    conn = psycopg2.connect(dbname=local_config.DB_NAME,
                            user=local_config.DB_USER,
                            password=local_config.DB_PASSWORD,
                            host=local_config.DB_HOST,
                            port=local_config.DB_PORT,
                            cursor_factory=RealDictCursor)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM places')
        records = cursor.fetchall()
    places = []
    for record in records:
        places.append({'id': str(record['id']),
                       'title': str(record['title']),
                       'image': str(record['image'])})
    return places


if __name__ == '__main__':
    print(get_places_from_db())

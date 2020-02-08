import json

import psycopg2
from psycopg2.extras import RealDictCursor

import config


def get_places_from_db():
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASSWORD,
                            host=config.DB_HOST,
                            port=config.DB_PORT,
                            cursor_factory=RealDictCursor)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM places')
        records = cursor.fetchall()
    places = []
    for record in records:
        places.append({'id': str(record['id']),
                       'title': str(record['title']),
                       'image': str(record['image']),
                       'timeShift': str(record['time_shift'])})
    return places


def get_place_from_db(place_id: int or str) -> dict:
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASSWORD,
                            host=config.DB_HOST,
                            port=config.DB_PORT,
                            cursor_factory=RealDictCursor)
    with conn.cursor() as cursor:
        cursor.execute(f'SELECT * FROM places WHERE id = {str(place_id)}')
        record = cursor.fetchall()
    return {'id': str(record[0]['id']),
            'title': record[0]['title'],
            'description': record[0]['description'],
            'time_shift': record[0]['time_shift']}


def save_route_to_db(timeline: list):
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASSWORD,
                            host=config.DB_HOST,
                            port=config.DB_PORT,
                            cursor_factory=RealDictCursor)
    with conn.cursor() as cursor:
        timeline = json.dumps(timeline)
        cursor.execute(f'INSERT INTO routes (timeline) VALUES (\'{timeline}\') RETURNING id')
        record_id = cursor.fetchone()[0]
    return record_id


if __name__ == '__main__':
    print(get_places_from_db())
    print(get_place_from_db(1))

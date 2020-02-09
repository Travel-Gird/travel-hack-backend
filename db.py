import json

import psycopg2
from psycopg2.extras import RealDictCursor

import config


def connection():
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASSWORD,
                            host=config.DB_HOST,
                            port=config.DB_PORT)
    conn.autocommit = True
    return conn


def get_places_from_db(city_name: str):
    with connection().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f'SELECT * FROM places '
                       f'WHERE city_id = {config.CITIES[city_name]}')
        records = cursor.fetchall()
    places = []
    for record in records:
        places.append({'id': str(record['id']),
                       'title': str(record['title']),
                       'image': str(record['image']),
                       'timeShift': str(record['time_shift'])})
    return places


def get_place_from_db(place_id: int or str) -> dict:
    with connection().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f'SELECT * FROM places WHERE id = {place_id}')
        record = cursor.fetchall()
    return {'id': str(record[0]['id']),
            'title': record[0]['title'],
            'description': record[0]['description'],
            'time_shift': record[0]['time_shift'],
            'latitude': record[0]['latitude'],
            'longitude': record[0]['longitude']}


def save_route_to_db(timeline: list) -> int:
    with connection().cursor(cursor_factory=RealDictCursor) as cursor:
        timeline = json.dumps(timeline)
        cursor.execute(f"INSERT INTO routes (timeline) "
                       f"VALUES ('{timeline}') RETURNING id")
        record_id = cursor.fetchone()['id']
    return record_id


def rate_route_in_db(user_facebook_id: int, route_id: int):
    with connection().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"INSERT INTO rates (user_facebook_id, route_id) "
                       f"VALUES ({str(user_facebook_id)}, {str(route_id)})")


def save_user_to_db(user_fb_id: str,
                    age: int,
                    gender: int,
                    location: int,
                    budget: int,
                    activity: int):
    with connection().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"INSERT INTO users (user_facebook_id, age, gender, location, budget, activity) "
            f"VALUES ({user_fb_id}, {age}, {gender}, "
            f"{location}, {budget}, {activity}) "
            f"ON CONFLICT (user_facebook_id) DO UPDATE SET "
            f"age = {age}, gender = {gender}, location = {location},"
            f"budget = {activity}, activity = {budget}")


def get_data_for_study():
    with connection().cursor() as cursor:
        cursor.execute('SELECT u.user_facebook_id, age, gender, location, '
                       'route_id FROM users u '
                       'LEFT JOIN (SELECT * FROM rates) r '
                       'ON r.user_facebook_id = u.user_facebook_id')
        records = cursor.fetchall()
        data_for_study = [list(record) for record in records]
        return data_for_study


if __name__ == '__main__':
    print(get_places_from_db())
    print(get_place_from_db(1))
    print(get_data_for_study())

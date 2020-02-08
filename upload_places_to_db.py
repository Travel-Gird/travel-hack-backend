import json
import re
import random
import psycopg2
from psycopg2.extras import RealDictCursor

import config

data = {}


def read_data(filename):
    with open(filename, 'r') as file:
        file_data = json.loads(file.read())
    return file_data


def upload_places_to_db(places_data):
    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASSWORD,
                            host=config.DB_HOST,
                            port=config.DB_PORT,
                            cursor_factory=RealDictCursor)
    with conn.cursor() as cursor:
        for city_id, places in places_data.items():
            time_shift = random.randint(1, 5)
            for place_data in places:
                title = place_data[0].replace("'", "''")
                image = place_data[3].replace("'", "''")
                description = place_data[2].replace("'", "''")
                cursor.execute(
                    f"INSERT INTO places "
                    f"(city_id, title, image, time_shift, "
                    f"description, latitude, longitude) "
                    f"VALUES ({city_id}, '{title}', '{image}', "
                    f"{time_shift}, '{description}', "
                    f"{place_data[4]}, {place_data[5]})"
                )
        conn.commit()


if __name__ == '__main__':
    data = read_data('assets/places.json')
    upload_places_to_db(data)

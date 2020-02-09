import os


TEST_USER_FB_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
TEST_USER_FB_ID = os.getenv('FACEBOOK_USER_ID', '')

HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', 5000))

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

CITIES = {'Moscow': 1,
          'London': 3,
          'Berlin': 4,
          'Paris': 5,
          'Beijing': 6,
          'Tokyo': 7,
          'Oslo': 8}

BUDGETS = {'Недорого': 1,
           'Комфорт': 2,
           'Шикануть': 3}

ACTIVITIES = {'Активный': 1,
              'Пляжный': 2,
              'С детьми': 3,
              'Экскурсионный': 4,
              'Ночная жизнь': 5}

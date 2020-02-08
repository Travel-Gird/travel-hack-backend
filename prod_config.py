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

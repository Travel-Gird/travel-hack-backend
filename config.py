import os


TEST_USER_FB_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
TEST_USER_FB_ID = os.getenv('FACEBOOK_USER_ID', '')

HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', 5000))

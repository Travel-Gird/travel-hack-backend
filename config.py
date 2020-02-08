import os


TEST_USER_FB_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
TEST_USER_FB_ID = os.getenv('FACEBOOK_USER_ID', '')

PORT = int(os.getenv('PORT', 5000))

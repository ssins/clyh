import os
BASE_DIR = os.getcwd()

# flask server
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 3333
FLASK_DEBUG = False

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ['txt']

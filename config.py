import os
from dotenv import load_dotenv

class Config():

    load_dotenv()

    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    ETSY_API_KEY = os.getenv('ETSY_API_KEY')

import os
from dotenv import load_dotenv

load_dotenv()
class Config():
    API_URL = os.getenv('API_URL')
    SECRET_KEY = os.getenv("SECRET_KEY") or 'you-will-never-guess'

import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    DEBUG = True
    SECRET_KEY = "aaaaaaaaasecret"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/app_db"
    CACHE_TYPE = 'simple'  # Use simple caching for demonstration purposes
    CACHE_DEFAULT_TIMEOUT = 300
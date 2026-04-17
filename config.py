import os
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "claveSecreta"
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Usar PyMySQL (está instalado en el entorno virtual) como driver de MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://leonardo:rootwan@127.0.0.1/ico801'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
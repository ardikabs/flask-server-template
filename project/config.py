
import os
import sys
import requests

''' Environment Variable Configuration '''
if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]           

class Config(object):
    SECRET_KEY = "this-really-need-to-be-changed"
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False
    
    # POSTGRESQL
    DB_USER = 'ancok125'
    DB_PASSWORD = 'l1nux1user'
    DB_NAME = 'cloud'
    DB_HOST = '172.18.69.17'
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_DATABASE_URL') or \
                            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    ## SQLITE
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                         f'sqlite:///{os.path.join(BASEDIR, "data-dev.db")}'

    ## CELERY CONFIG
    CELERY_BROKER_URL = "redis://172.18.69.17:6379/0"
    CELERY_RESULT_BACKEND = "redis://172.18.69.17:6379/0"


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    
    @classmethod
    def init_app(cls, app):
        print ("RUNNING ON DEBUG MODE")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


    @classmethod
    def init_app(cls, app):
        print ("RUNNING ON TESTING MODE")



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
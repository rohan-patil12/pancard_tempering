import os

class Config(object):
    DEBUG = False
    TESTING = False
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'pianalytix'
    UPLOADS = os.path.join(basedir, "app", "static", "uploads")

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

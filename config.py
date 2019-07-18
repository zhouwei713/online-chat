# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:32
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hardtohard'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'chat.sqlite3')
    EXPARE_TIME = 604800  # 7 天
    JOBS = []
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }

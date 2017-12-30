#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path

class Config(object):
    DEBUG = False
    PORT = 18081
    HOST = '0.0.0.0'
    PROJECT_ROOT = path.abspath(path.dirname(__file__))
    TEMPLATE_FOLDER = path.join(PROJECT_ROOT, 'templates')
    JSON_ADD_STATUS = False
    MYSQL_DATABASE_HOST = '127.0.0.1'
    MYSQL_DATABASE_DB = 'default_db'
    MYSQL_DATABASE_USER = 'default_user'
    MYSQL_DATABASE_PASSWORD = 'password'

class Development(Config):
    DEBUG = True
    SECRET_KEY = 'development'

class Production(Config):
    pass

class Testing(Config):
    TESTING = True
    SECRET_KEY = 'testing'